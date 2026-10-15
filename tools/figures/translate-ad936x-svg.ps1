param(
    [Parameter(Mandatory=$true)][string]$SourceSvg,
    [string]$OutputDirectory = (Join-Path $PSScriptRoot '../../docs/assets/ad936x')
)
$ErrorActionPreference = 'Stop'
New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null
Copy-Item -LiteralPath $SourceSvg -Destination (Join-Path $OutputDirectory 'ad9361-original.svg')
[xml]$svg = Get-Content -Raw -Encoding utf8 -LiteralPath $SourceSvg
$translations = @{
    'Baseband'='基带'; 'Rx Channel 1'='接收通道 1'; 'Rx Channel 2'='接收通道 2'
    'Tx Channel 1'='发射通道 1'; 'Tx Channel 2'='发射通道 2'; '12-bit'='12 位'
    '10-bit'='10 位'; 'Dual'='双路'; 'Reset'='复位'; 'CTRL'='控制'
    'DIV'='分频'; 'Calibration and'='校准与'; 'Correction'='校正'
    'Temperature'='温度'; 'Sensor'='传感器'; 'Enable State'='使能状态机'
    'Machine (ENSM)'='（ENSM）'; 'Automatic'='自动'; 'Gain'='增益'; 'Control'='控制'
    '□ Manual'='□ 手动'; '□ Slow'='□ 慢速'; '□ Fast'='□ 快速'
    'Phase'='正交'; 'Splitter'='分相器'
    'RF Channel Bandwidth'='射频通道带宽'; 'Rx Decimation '='接收抽取 '
    'Tx Interpolation '='发射插值 '; 'Digital Filtering and Equalization'='数字滤波与均衡'
    'Input Mux'='输入选择'; 'Output Mux'='输出选择'; 'ATTN'='衰减'
    'CMOS / LVDS INTERFACE'='CMOS / LVDS 接口'; 'LOOP'='内部'; 'BACK'='回环'
    'PN &'='伪随机与'; 'BIST'='自测试'; 'RADIO'='射频'; 'SWITCHING'='切换'
    'Rx'='接收'; 'Tx'='发射'; 'Mon'='监测'; 'RxA'='接收 A'; 'RxB'='接收 B'
    'RxC'='接收 C'; 'TxA'='发射 A'; 'TxB'='发射 B'
    'Ch1 I/Q'='通道1 I/Q'; 'Ch2 I/Q'='通道2 I/Q'
    'Rx 61.44 MSPS'='接收 61.44 MSPS'; 'Tx 61.44 MSPS'='发射 61.44 MSPS'
    'AUX ADC'='辅助 ADC'; 'AUX DAC'='辅助 DAC'
}
# Replace visible labels only; preserve geometry, identifiers and pin names.
$count = 0
foreach ($node in $svg.SelectNodes('//*[local-name()="tspan"]')) {
    if ($translations.ContainsKey($node.InnerText)) {
        $node.InnerText = $translations[$node.InnerText]
        $style = $node.GetAttribute('style') -replace 'font-family:[^;]+', 'font-family:Microsoft YaHei,SimHei,sans-serif'
        $node.SetAttribute('style', $style)
        $count++
    }
}
# The original stacked English AGC labels have insufficient leading for Chinese glyphs.
foreach ($id in @('text3191-8-1-2', 'text3191-8-1-2-5')) {
    $text = $svg.SelectSingleNode("//*[@id='$id']")
    $spans = @($text.SelectNodes('./*[local-name()="tspan"]'))
    $spans[0].InnerText = $(if ($id -eq 'text3191-8-1-2') { '自动增益控制' } else { '□ 手动  □ 慢速  □ 快速' })
    $spans[0].SetAttribute('y', '-159.82501')
    for ($i=1; $i -lt $spans.Count; $i++) { $spans[$i].InnerText = '' }
}
$svg.DocumentElement.SetAttribute('viewBox', '0 0 1128.3628 782')
$svg.Save((Join-Path $OutputDirectory 'ad9361-zh.svg'))
Write-Output "Translated $count SVG labels."
