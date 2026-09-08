<#
  Regenerates the site's hosted favicon files from their canonical SVG sources.

  Google Search will not display a favicon supplied as an inline data: URI —
  it needs a real file at a stable, separately crawlable URL. These files are
  that. Run this only when a source design in $Designs below changes; the
  output is committed to the repo root and served from there.

  Usage:  powershell -File scripts/gen_favicons.ps1
#>

Add-Type -AssemblyName System.Drawing

$Root = Split-Path -Parent $PSScriptRoot

# The two designs, transcribed verbatim from the SVGs at the repo root.
# Keep these in lockstep with favicon.svg / favicon-learning.svg.
$Designs = @(
  @{
    Prefix = 'favicon'          # site-wide: navy "SC" monogram
    Bg     = '#0B1F3A'
    Kind   = 'monogram'
    Fg     = '#2A7FD4'
  },
  @{
    Prefix = 'favicon-learning' # /learning/: terracotta open book
    Bg     = '#a5402d'
    Kind   = 'book'
    Fg     = '#fdfbf5'
  }
)

function New-Icon {
  param([hashtable]$Design, [int]$size)

  $s   = $size / 32.0
  $bg  = [System.Drawing.ColorTranslator]::FromHtml($Design.Bg)
  $fg  = [System.Drawing.ColorTranslator]::FromHtml($Design.Fg)
  $bmp = New-Object System.Drawing.Bitmap($size, $size, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
  $g   = [System.Drawing.Graphics]::FromImage($bmp)
  $g.SmoothingMode     = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
  $g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
  $g.PixelOffsetMode   = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
  $g.Clear([System.Drawing.Color]::Transparent)

  # <rect width='32' height='32' rx='6' fill='$Bg'/>
  $dia = 12.0 * $s
  $w = [float]$size
  $p = New-Object System.Drawing.Drawing2D.GraphicsPath
  $p.AddArc(0, 0, $dia, $dia, 180, 90)
  $p.AddArc($w - $dia, 0, $dia, $dia, 270, 90)
  $p.AddArc($w - $dia, $w - $dia, $dia, $dia, 0, 90)
  $p.AddArc(0, $w - $dia, $dia, $dia, 90, 90)
  $p.CloseFigure()
  $b = New-Object System.Drawing.SolidBrush($bg)
  $g.FillPath($b, $p)
  $b.Dispose(); $p.Dispose()

  if ($Design.Kind -eq 'monogram') {
    # <text x='16' y='22' font-family='Georgia,serif' font-size='18'
    #       font-weight='bold' fill='$Fg' text-anchor='middle'>SC</text>
    $em     = 18.0 * $s
    $fam    = New-Object System.Drawing.FontFamily('Georgia')
    $style  = [System.Drawing.FontStyle]::Bold
    $ascent = $em * $fam.GetCellAscent($style) / $fam.GetEmHeight($style)
    $top    = (22.0 * $s) - $ascent          # SVG y= is the baseline; GDI+ wants the cell top

    $fmt = New-Object System.Drawing.StringFormat([System.Drawing.StringFormat]::GenericTypographic)
    $fmt.Alignment     = [System.Drawing.StringAlignment]::Center
    $fmt.LineAlignment = [System.Drawing.StringAlignment]::Near
    $fmt.FormatFlags   = [System.Drawing.StringFormatFlags]::NoWrap

    $box = New-Object System.Drawing.RectangleF([float]((16.0 * $s) - $size), [float]$top, [float]($size * 2), [float]($em * 2))
    $tp  = New-Object System.Drawing.Drawing2D.GraphicsPath
    $tp.AddString('SC', $fam, [int]$style, [float]$em, $box, $fmt)
    $tb  = New-Object System.Drawing.SolidBrush($fg)
    $g.FillPath($tb, $tp)
    $tb.Dispose(); $tp.Dispose(); $fmt.Dispose(); $fam.Dispose()
  }
  else {
    # <path d='M16 10 C13.5 8 9.5 8 7 9 V23 C9.5 22 13.5 22 16 24
    #          C18.5 22 22.5 22 25 23 V9 C22.5 8 18.5 8 16 10 Z' fill='$Fg'/>
    $bp = New-Object System.Drawing.Drawing2D.GraphicsPath
    $bp.AddBezier(16*$s,10*$s, 13.5*$s,8*$s,  9.5*$s,8*$s,   7*$s,9*$s)
    $bp.AddLine(  7*$s, 9*$s,   7*$s,23*$s)
    $bp.AddBezier( 7*$s,23*$s,  9.5*$s,22*$s, 13.5*$s,22*$s, 16*$s,24*$s)
    $bp.AddBezier(16*$s,24*$s, 18.5*$s,22*$s, 22.5*$s,22*$s, 25*$s,23*$s)
    $bp.AddLine( 25*$s,23*$s,  25*$s, 9*$s)
    $bp.AddBezier(25*$s, 9*$s, 22.5*$s,8*$s,  18.5*$s,8*$s,  16*$s,10*$s)
    $bp.CloseFigure()
    $bb = New-Object System.Drawing.SolidBrush($fg)
    $g.FillPath($bb, $bp)
    $bb.Dispose(); $bp.Dispose()

    # <path d='M16 10 V24' stroke='$Bg' stroke-width='1.5'/>  — the spine
    $pen = New-Object System.Drawing.Pen($bg, [float](1.5 * $s))
    $g.DrawLine($pen, [float](16*$s), [float](10*$s), [float](16*$s), [float](24*$s))
    $pen.Dispose()
  }

  $g.Dispose()
  return $bmp
}

# A 32-bit BGRA DIB entry (bottom-up XOR rows + an all-zero AND mask).
# Preferred over PNG-in-ICO here: universally readable by old and new decoders.
function Get-DibBytes([System.Drawing.Bitmap]$bmp) {
  $w = $bmp.Width; $h = $bmp.Height
  $ms = New-Object System.IO.MemoryStream
  $bw = New-Object System.IO.BinaryWriter($ms)
  $bw.Write([uint32]40); $bw.Write([int32]$w); $bw.Write([int32]($h * 2))
  $bw.Write([uint16]1);  $bw.Write([uint16]32)
  $bw.Write([uint32]0);  $bw.Write([uint32]($w * $h * 4))
  $bw.Write([int32]0);   $bw.Write([int32]0)
  $bw.Write([uint32]0);  $bw.Write([uint32]0)

  $rect = New-Object System.Drawing.Rectangle(0, 0, $w, $h)
  $data = $bmp.LockBits($rect, [System.Drawing.Imaging.ImageLockMode]::ReadOnly, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
  $buf  = New-Object byte[] ($data.Stride * $h)
  [System.Runtime.InteropServices.Marshal]::Copy($data.Scan0, $buf, 0, $buf.Length)
  $bmp.UnlockBits($data)
  for ($y = $h - 1; $y -ge 0; $y--) { $bw.Write($buf, $y * $data.Stride, $w * 4) }

  $maskRow = [int][Math]::Floor((($w + 31) / 32)) * 4
  $bw.Write((New-Object byte[] ($maskRow * $h)), 0, $maskRow * $h)
  $bw.Flush()
  return $ms.ToArray()
}

foreach ($Design in $Designs) {
  foreach ($sz in 48, 192) {
    $b = New-Icon $Design $sz
    $p = Join-Path $Root "$($Design.Prefix)-${sz}x${sz}.png"
    $b.Save($p, [System.Drawing.Imaging.ImageFormat]::Png); $b.Dispose()
    "wrote $p"
  }

  $sizes  = 16, 32, 48
  $images = @()
  foreach ($sz in $sizes) { $b = New-Icon $Design $sz; $images += ,(Get-DibBytes $b); $b.Dispose() }

  $ico = Join-Path $Root "$($Design.Prefix).ico"
  $fs  = [System.IO.File]::Create($ico)
  $bw  = New-Object System.IO.BinaryWriter($fs)
  $bw.Write([uint16]0); $bw.Write([uint16]1); $bw.Write([uint16]$sizes.Count)
  $offset = 6 + (16 * $sizes.Count)
  for ($i = 0; $i -lt $sizes.Count; $i++) {
    $bytes = $images[$i]
    $bw.Write([byte]$sizes[$i]); $bw.Write([byte]$sizes[$i])
    $bw.Write([byte]0); $bw.Write([byte]0)
    $bw.Write([uint16]1); $bw.Write([uint16]32)
    $bw.Write([uint32]$bytes.Length); $bw.Write([uint32]$offset)
    $offset += $bytes.Length
  }
  foreach ($bytes in $images) { $bw.Write($bytes, 0, $bytes.Length) }
  $bw.Flush(); $bw.Close(); $fs.Close()
  "wrote $ico"
}
