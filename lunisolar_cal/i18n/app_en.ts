<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="en_US" sourcelanguage="zh_CN">
<context>
    <name>CalendarErrors</name>
    <message>
        <location filename="../core.py" line="60"/>
        <source>年、月、日必须是整数。</source>
        <translation>Year, month and day must be integers.</translation>
    </message>
    <message>
        <location filename="../core.py" line="63"/>
        <source>输入年份必须在{min_year}～{max_year}之间。</source>
        <translation>The input year must be between {min_year} and {max_year}.</translation>
    </message>
    <message>
        <location filename="../core.py" line="67"/>
        <source>月份必须在1～12之间。</source>
        <translation>Month must be between 1 and 12.</translation>
    </message>
    <message>
        <location filename="../core.py" line="70"/>
        <source>日期必须在1～{max_day}之间。</source>
        <translation>Day must be between 1 and {max_day}.</translation>
    </message>
    <message>
        <location filename="../core.py" line="78"/>
        <source>1582年10月5日至14日属于改历缺口，在本程序采用的历法中不存在。</source>
        <translation>Dates from October 5 to 14, 1582 are in the calendar reform gap.</translation>
    </message>
    <message>
        <location filename="../core.py" line="86"/>
        <source>无法解析公历日期：{detail}</source>
        <translation>Unable to parse the solar date: {detail}</translation>
    </message>
    <message>
        <location filename="../core.py" line="91"/>
        <source>公历日期不存在，请检查该月的天数和闰年规则。</source>
        <translation>The solar date does not exist. Check the month length and leap-year rule.</translation>
    </message>
    <message>
        <location filename="../core.py" line="102"/>
        <source>is_leap 必须是布尔值 True 或 False。</source>
        <translation>is_leap must be a boolean (True or False).</translation>
    </message>
    <message>
        <location filename="../core.py" line="110"/>
        <source>无法查询农历月份：{detail}</source>
        <translation>Unable to query the lunisolar month: {detail}</translation>
    </message>
    <message>
        <location filename="../core.py" line="115"/>
        <source>{year}年不存在闰{month}月。</source>
        <translation>Year {year} has no leap month {month}.</translation>
    </message>
    <message>
        <location filename="../core.py" line="120"/>
        <source>{year}年闰{month}月只有{days}天。</source>
        <translation>Year {year}, leap month {month} has only {days} days.</translation>
    </message>
    <message>
        <location filename="../core.py" line="122"/>
        <source>{year}年{month}月只有{days}天。</source>
        <translation>Year {year}, month {month} has only {days} days.</translation>
    </message>
    <message>
        <location filename="../core.py" line="130"/>
        <source>无法解析农历日期：{detail}</source>
        <translation>Unable to parse the lunisolar date: {detail}</translation>
    </message>
    <message>
        <location filename="../core.py" line="134"/>
        <source>农历日期往返校验不一致，请核对年月日及闰月信息。</source>
        <translation>The lunisolar round-trip check failed. Check the date and leap-month setting.</translation>
    </message>
    <message>
        <location filename="../formatting.py" line="74"/>
        <source>输入有误：{reason}</source>
        <translation>Invalid input: {reason}</translation>
    </message>
</context>
<context>
    <name>DateFormatting</name>
    <message>
        <location filename="../formatting.py" line="35"/>
        <source>农历：{date}</source>
        <translation>Lunisolar: {date}</translation>
    </message>
    <message>
        <location filename="../formatting.py" line="40"/>
        <source>农历：{year}年闰{month}月{day}日</source>
        <translation>Lunisolar: year {year}, leap month {month}, day {day}</translation>
    </message>
    <message>
        <location filename="../formatting.py" line="44"/>
        <source>农历：{year}年{month}月{day}日</source>
        <translation>Lunisolar: year {year}, month {month}, day {day}</translation>
    </message>
    <message>
        <location filename="../formatting.py" line="56"/>
        <source>公历：{year}年{month}月{day}日</source>
        <translation>Solar: {year}-{month}-{day}</translation>
    </message>
</context>
<context>
    <name>LsConvWindow</name>
    <message>
        <location filename="../ui/lsconv.ui" line="14"/>
        <source>公农历转换</source>
        <translation>Solar-Lunisolar Converter</translation>
    </message>
    <message>
        <location filename="../ui/lsconv.ui" line="45"/>
        <source>请输入需要转换的日期：</source>
        <translation>Enter a date to convert:</translation>
    </message>
    <message>
        <location filename="../ui/lsconv.ui" line="73"/>
        <source>界面语言：</source>
        <translation>Language:</translation>
    </message>
    <message>
        <location filename="../ui/lsconv.ui" line="93"/>
        <source>简体中文</source>
        <translation>简体中文</translation>
    </message>
    <message>
        <location filename="../ui/lsconv.ui" line="98"/>
        <source>English</source>
        <translation>English</translation>
    </message>
    <message>
        <location filename="../ui/lsconv.ui" line="103"/>
        <location filename="../ui/lsconv.ui" line="122"/>
        <source>跟随系统</source>
        <translation>Follow system</translation>
    </message>
    <message>
        <location filename="../ui/lsconv.ui" line="111"/>
        <source>主题：</source>
        <translation>Theme:</translation>
    </message>
    <message>
        <location filename="../ui/lsconv.ui" line="127"/>
        <source>浅色</source>
        <translation>Light</translation>
    </message>
    <message>
        <location filename="../ui/lsconv.ui" line="132"/>
        <source>深色</source>
        <translation>Dark</translation>
    </message>
    <message>
        <location filename="../ui/lsconv.ui" line="137"/>
        <source>Latte（浅色）</source>
        <translation>Latte (Light)</translation>
    </message>
    <message>
        <location filename="../ui/lsconv.ui" line="142"/>
        <source>Frappé（深色）</source>
        <translation>Frappé (Dark)</translation>
    </message>
    <message>
        <location filename="../ui/lsconv.ui" line="147"/>
        <source>Macchiato（深色）</source>
        <translation>Macchiato (Dark)</translation>
    </message>
    <message>
        <location filename="../ui/lsconv.ui" line="152"/>
        <source>Mocha（深色）</source>
        <translation>Mocha (Dark)</translation>
    </message>
    <message>
        <location filename="../ui/lsconv.ui" line="191"/>
        <source>输入历法：</source>
        <translation>Input calendar:</translation>
    </message>
    <message>
        <location filename="../ui/lsconv.ui" line="205"/>
        <source>公历</source>
        <translation>Solar</translation>
    </message>
    <message>
        <location filename="../ui/lsconv.ui" line="210"/>
        <source>农历</source>
        <translation>Lunisolar</translation>
    </message>
    <message>
        <location filename="../ui/lsconv.ui" line="240"/>
        <source>中文农历表示</source>
        <translation>Chinese lunisolar notation</translation>
    </message>
    <message>
        <location filename="../ui/lsconv.ui" line="272"/>
        <source>今天</source>
        <translation>Today</translation>
    </message>
    <message>
        <location filename="../ui/lsconv.ui" line="295"/>
        <source>年份：</source>
        <translation>Year:</translation>
    </message>
    <message>
        <location filename="../ui/lsconv.ui" line="308"/>
        <source>月份：</source>
        <translation>Month:</translation>
    </message>
    <message>
        <location filename="../ui/lsconv.ui" line="321"/>
        <source>日期：</source>
        <translation>Day:</translation>
    </message>
    <message>
        <location filename="../ui/lsconv.ui" line="367"/>
        <source>闰月（农历）</source>
        <translation>Leap month (lunisolar)</translation>
    </message>
    <message>
        <location filename="../ui/lsconv.ui" line="400"/>
        <source>转换</source>
        <translation>Convert</translation>
    </message>
    <message>
        <location filename="../gui.py" line="29"/>
        <location filename="../gui.py" line="100"/>
        <location filename="../gui.py" line="130"/>
        <location filename="../ui/lsconv.ui" line="420"/>
        <source>复制结果</source>
        <translation>Copy result</translation>
    </message>
    <message>
        <location filename="../gui.py" line="122"/>
        <source>已复制</source>
        <translation>Copied</translation>
    </message>
    <message>
        <location filename="../gui.py" line="128"/>
        <location filename="../ui/lsconv.ui" line="451"/>
        <source>等待转换</source>
        <translation>Waiting for conversion</translation>
    </message>
    <message>
        <location filename="../gui.py" line="172"/>
        <source>&lt;h3&gt;公农历转换&lt;/h3&gt;&lt;p&gt;版本：{version}&lt;br&gt;作者：朝曦凝云AsahiKumo&lt;br&gt;项目许可证：MIT&lt;/p&gt;&lt;p&gt;基于 sxtwl 的公历、农历双向转换工具。&lt;/p&gt;&lt;p&gt;开发中使用 OpenAI Codex 辅助编程、调试、文档整理和图标制作。&lt;/p&gt;&lt;p&gt;&lt;a href=&quot;https://github.com/AsahiKumo/LunisolarCal&quot;&gt;项目主页&lt;/a&gt;&lt;/p&gt;</source>
        <translation>&lt;h3&gt;Solar-Lunisolar Converter&lt;/h3&gt;
&lt;p&gt;Version: {version}&lt;br&gt;Author: 朝曦凝云AsahiKumo&lt;br&gt;Project license: MIT&lt;/p&gt;
&lt;p&gt;A solar-lunisolar date conversion tool based on sxtwl.&lt;/p&gt;
&lt;p&gt;Developed with assistance from OpenAI Codex for coding, debugging, documentation and icons.&lt;/p&gt;
&lt;p&gt;&lt;a href=&quot;https://github.com/AsahiKumo/LunisolarCal&quot;&gt;Project homepage&lt;/a&gt;&lt;/p&gt;</translation>
    </message>
    <message>
        <location filename="../gui.py" line="179"/>
        <location filename="../ui/lsconv.ui" line="179"/>
        <source>关于</source>
        <translation>About</translation>
    </message>
    <message>
        <location filename="../gui.py" line="182"/>
        <source>确定</source>
        <translation>OK</translation>
    </message>
    <message>
        <location filename="../gui.py" line="186"/>
        <location filename="../gui.py" line="207"/>
        <source>许可说明</source>
        <translation>Licenses</translation>
    </message>
    <message>
        <location filename="../gui.py" line="199"/>
        <source>项目许可证（MIT）</source>
        <translation>Project license (MIT)</translation>
    </message>
    <message>
        <location filename="../gui.py" line="200"/>
        <source>第三方组件与许可</source>
        <translation>Third-party components and licenses</translation>
    </message>
    <message>
        <location filename="../gui.py" line="214"/>
        <source>关闭</source>
        <translation>Close</translation>
    </message>
    <message>
        <location filename="../gui.py" line="224"/>
        <source>无法读取文件：{path}
{error}</source>
        <translation>Unable to read file: {path}
{error}</translation>
    </message>
</context>
</TS>
