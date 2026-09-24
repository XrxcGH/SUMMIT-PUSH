param([string]$Path)
[xml]$svg = Get-Content -Raw $Path
$vb = $svg.svg.viewBox -split '\s+'
$vbW = [double]$vb[2]; $vbH = [double]$vb[3]
$texts = @(); $lines = @(); $rects = @(); $others = @()

function Get-Nodes($node) {
  foreach ($child in $node.ChildNodes) {
    if ($child.NodeType -ne 'Element') { continue }
    $script:ctx = $child
    switch ($child.LocalName) {
      'text' {
        $fs = 11.0
        if ($child.GetAttribute('font-size')) { $fs = [double]($child.GetAttribute('font-size') -replace 'px','') }
        elseif ($child.GetAttribute('class') -match 'vtitle') { $fs = 14 }
        elseif ($child.GetAttribute('class') -match 'dimt|lbl') { $fs = 11 }
        $str = $child.InnerText
        $w = 0.58 * $fs * $str.Length
        $x = [double]$child.GetAttribute('x'); $y = [double]$child.GetAttribute('y')
        $anchor = $child.GetAttribute('text-anchor')
        $rot = ($child.GetAttribute('transform') -match 'rotate')
        switch ($anchor) {
          'middle' { $x0 = $x - $w/2; $x1 = $x + $w/2 }
          'end'    { $x0 = $x - $w;   $x1 = $x }
          default  { $x0 = $x;        $x1 = $x + $w }
        }
        $script:texts += [pscustomobject]@{ str=$str; x0=$x0; x1=$x1; y0=$y-$fs; y1=$y+2; rot=$rot; fs=$fs }
      }
      'line' {
        $script:lines += [pscustomobject]@{
          x1=[double]$child.GetAttribute('x1'); y1=[double]$child.GetAttribute('y1')
          x2=[double]$child.GetAttribute('x2'); y2=[double]$child.GetAttribute('y2')
          cls=$child.GetAttribute('class'); dash=$child.GetAttribute('stroke-dasharray')
          rot=($child.GetAttribute('transform') -match 'rotate')
        }
      }
      'rect' {
        $script:rects += [pscustomobject]@{
          x=[double]$child.GetAttribute('x'); y=[double]$child.GetAttribute('y')
          w=[double]$child.GetAttribute('width'); h=[double]$child.GetAttribute('height')
          fill=$child.GetAttribute('fill'); rot=(($child.ParentNode.GetAttribute('transform') + $child.GetAttribute('transform')) -match 'rotate')
        }
      }
      default { }
    }
    Get-Nodes $child
  }
}
Get-Nodes $svg.svg

$issues = @()
# 1. out of viewBox
foreach ($t in $texts) {
  if (-not $t.rot -and ($t.x0 -lt 0 -or $t.x1 -gt $vbW -or $t.y0 -lt 0 -or $t.y1 -gt $vbH)) {
    $issues += "VIEWBOX: text '$($t.str.Substring(0,[Math]::Min(45,$t.str.Length)))' bbox [$([int]$t.x0)..$([int]$t.x1)] x [$([int]$t.y0)..$([int]$t.y1)] exceeds viewBox ${vbW}x${vbH}"
  }
}
foreach ($r in $rects) {
  if (-not $r.rot -and ($r.x -lt 0 -or ($r.x+$r.w) -gt $vbW -or $r.y -lt 0 -or ($r.y+$r.h) -gt $vbH)) {
    $issues += "VIEWBOX: rect at ($($r.x),$($r.y)) ${($r.w)}x${($r.h)} exceeds viewBox"
  }
}
# 2. text-vs-text overlap (non-rotated only)
for ($i=0; $i -lt $texts.Count; $i++) {
  for ($j=$i+1; $j -lt $texts.Count; $j++) {
    $a=$texts[$i]; $b=$texts[$j]
    if ($a.rot -or $b.rot) { continue }
    if ($a.x0 -lt ($b.x1-2) -and $b.x0 -lt ($a.x1-2) -and $a.y0 -lt ($b.y1-2) -and $b.y0 -lt ($a.y1-2)) {
      $issues += "TEXT-TEXT: '$($a.str.Substring(0,[Math]::Min(40,$a.str.Length)))' overlaps '$($b.str.Substring(0,[Math]::Min(40,$b.str.Length)))'"
    }
  }
}
# 3. text-vs-line: straight H/V lines crossing a text bbox (ignore a line's own nearby label: skip if line endpoint within 4px of bbox edge only touching)
foreach ($t in $texts) {
  if ($t.rot) { continue }
  foreach ($l in $lines) {
    if ($l.rot) { continue }
    if ([math]::Abs($l.x1-$l.x2) -lt 0.01) { # vertical
      $lx=$l.x1; $ly0=[math]::Min($l.y1,$l.y2); $ly1=[math]::Max($l.y1,$l.y2)
      if ($lx -gt ($t.x0+2) -and $lx -lt ($t.x1-2) -and $ly0 -lt ($t.y1-2) -and $ly1 -gt ($t.y0+2)) {
        $issues += "TEXT-LINE: v-line x=$lx crosses text '$($t.str.Substring(0,[Math]::Min(40,$t.str.Length)))'"
      }
    } elseif ([math]::Abs($l.y1-$l.y2) -lt 0.01) { # horizontal
      $ly=$l.y1; $lx0=[math]::Min($l.x1,$l.x2); $lx1=[math]::Max($l.x1,$l.x2)
      if ($ly -gt ($t.y0+3) -and $ly -lt ($t.y1-3) -and $lx0 -lt ($t.x1-2) -and $lx1 -gt ($t.x0+2)) {
        $issues += "TEXT-LINE: h-line y=$ly crosses text '$($t.str.Substring(0,[Math]::Min(40,$t.str.Length)))'"
      }
    }
  }
}
# 4. text straddling a rect edge (text partially inside, partially outside a stroked rect) — skip fills used as backgrounds
foreach ($t in $texts) {
  if ($t.rot) { continue }
  foreach ($r in $rects) {
    if ($r.rot -or $r.w -gt 900) { continue }
    $rx0=$r.x; $rx1=$r.x+$r.w; $ry0=$r.y; $ry1=$r.y+$r.h
    $ix = ($t.x0 -lt $rx1 -and $rx0 -lt $t.x1); $iy = ($t.y0 -lt $ry1 -and $ry0 -lt $t.y1)
    if ($ix -and $iy) {
      $inside = ($t.x0 -ge $rx0-2 -and $t.x1 -le $rx1+2 -and $t.y0 -ge $ry0-2 -and $t.y1 -le $ry1+2)
      $edgeCross = ((($t.x0 -lt $rx0) -and ($t.x1 -gt $rx0+3)) -or (($t.x0 -lt $rx1-3) -and ($t.x1 -gt $rx1)) -or (($t.y0 -lt $ry0) -and ($t.y1 -gt $ry0+3)) -or (($t.y0 -lt $ry1-3) -and ($t.y1 -gt $ry1)))
      if (-not $inside -and $edgeCross) {
        $issues += "TEXT-RECT: text '$($t.str.Substring(0,[Math]::Min(40,$t.str.Length)))' straddles rect edge at ($rx0,$ry0) ${($r.w)}x${($r.h)}"
      }
    }
  }
}
"=== $([System.IO.Path]::GetFileName($Path)) : $($issues.Count) potential issues ==="
$issues | Sort-Object -Unique
