# -*- coding: utf-8 -*-
"""生成 build/course_14.json:驱动开发 28 节的导读 + 分层资料 + 5 个验收关卡。"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

GS  = 'https://learn.microsoft.com/zh-cn/windows-hardware/drivers/gettingstarted/'
K   = 'https://learn.microsoft.com/zh-cn/windows-hardware/drivers/kernel/'
DDI = 'https://learn.microsoft.com/zh-cn/windows-hardware/drivers/ddi/'
DBG = 'https://learn.microsoft.com/zh-cn/windows-hardware/drivers/debugger/'
DRV = 'https://learn.microsoft.com/zh-cn/windows-hardware/drivers/'
CN  = 'https://www.cnblogs.com/'
PE  = 'https://learn.microsoft.com/zh-cn/windows/win32/debug/pe-format'

# ── 资料池:[标题, URL, 分层]  主学=先看这份 / 原文=一手权威 / 实操=能上手跑 / 延伸=想深入再看 ──
R = {
 # 概念主学(微软官方中文 + 博客园)
 'gs_all':  ['微软 · 所有驱动开发者都要懂的核心概念', GS + 'concepts-and-knowledge-for-all-driver-developers', '主学'],
 'gs_start':['微软 · 编写你的第一个驱动',            GS + 'writing-your-first-driver', '主学'],
 'gs_over': ['微软 · 驱动开发入门总览',              GS, '主学'],
 'gs_tmpl': ['微软 · 用模板新建 KMDF 驱动工程',      GS + 'writing-a-kmdf-driver-based-on-a-template', '实操'],
 'wdk':     ['微软 · 下载安装 WDK',                 DRV + 'download-the-wdk', '实操'],
 'wdk2':    ['微软 · WDK 历史版本下载',             DRV + 'other-wdk-downloads', '延伸'],
 'wdm':     ['微软 · WDM 驱动模型导论',             K + 'introduction-to-wdm', '主学'],
 'entry':   ['微软 · 编写 DriverEntry 例程',        K + 'writing-a-driverentry-routine', '原文'],
 'drvobj':  ['微软 · DRIVER_OBJECT 驱动对象结构',   DDI + 'wdm/ns-wdm-_driver_object', '原文'],
 'devobj':  ['微软 · DEVICE_OBJECT 设备对象结构',   DDI + 'wdm/ns-wdm-_device_object', '原文'],
 'devstk':  ['微软 · 设备对象与设备栈',             K + 'device-objects-and-device-stacks', '主学'],
 'named':   ['微软 · 命名设备对象',                 K + 'named-device-objects', '主学'],
 'crdev':   ['微软 · 创建设备对象',                 K + 'creating-a-device-object', '实操'],
 # 内存 / 字符串 / 链表
 'allocsp': ['微软 · 分配系统空间内存',             K + 'allocating-system-space-memory', '主学'],
 'expool2': ['微软 · ExAllocatePool2 分配池内存',   DDI + 'wdm/nf-wdm-exallocatepool2', '原文'],
 'expoolt': ['微软 · ExAllocatePoolWithTag(旧接口)', DDI + 'wdm/nf-wdm-exallocatepoolwithtag', '延伸'],
 'exfree':  ['微软 · ExFreePool 释放池内存',        DDI + 'wdm/nf-wdm-exfreepool', '原文'],
 'rtlcopy': ['微软 · RtlCopyMemory',                DDI + 'wdm/nf-wdm-rtlcopymemory', '原文'],
 'rtlzero': ['微软 · RtlZeroMemory',                DDI + 'wdm/nf-wdm-rtlzeromemory', '原文'],
 'ustr':    ['微软 · UNICODE_STRING 结构',          DDI + 'wudfwdm/ns-wudfwdm-_unicode_string', '原文'],
 'rtlinit': ['微软 · RtlInitUnicodeString',         DDI + 'wdm/nf-wdm-rtlinitunicodestring', '原文'],
 'rtlu2a':  ['微软 · RtlUnicodeStringToAnsiString', DDI + 'wdm/nf-wdm-rtlunicodestringtoansistring', '原文'],
 'list':    ['微软 · 单向与双向链表',               K + 'singly-and-doubly-linked-lists', '主学'],
 'listhd':  ['微软 · InitializeListHead',           DDI + 'wdm/nf-wdm-initializelisthead', '原文'],
 'insert':  ['微软 · InsertHeadList',               DDI + 'wdm/nf-wdm-insertheadlist', '原文'],
 'mmsys':   ['微软 · MmGetSystemRoutineAddress 取内核函数地址', DDI + 'wdm/nf-wdm-mmgetsystemroutineaddress', '原文'],
 'ntzw':    ['微软 · Nt 与 Zw 版本例程的区别',      K + 'using-nt-and-zw-versions-of-the-native-system-services-routines', '延伸'],
 # IRP / 派遣 / 通信
 'irp':     ['微软 · 处理 IRP',                     K + 'handling-irps', '主学'],
 'irpmj':   ['微软 · IRP 主功能码 IRP_MJ_*',        K + 'irp-major-function-codes', '原文'],
 'disp':    ['微软 · 编写派遣例程',                 K + 'writing-dispatch-routines', '主学'],
 'complete':['微软 · 完成 IRP(IoCompleteRequest)', K + 'completing-irps', '原文'],
 'iostk':   ['微软 · IoGetCurrentIrpStackLocation', DDI + 'wdm/nf-wdm-iogetcurrentirpstacklocation', '原文'],
 'ioctldef':['微软 · 定义 I/O 控制码 CTL_CODE',     K + 'defining-i-o-control-codes', '主学'],
 'ioctlbuf':['微软 · IOCTL 的缓冲区描述',           K + 'buffer-descriptions-for-i-o-control-codes', '原文'],
 'access':  ['微软 · 访问数据缓冲区的三种方法',     K + 'methods-for-accessing-data-buffers', '主学'],
 'buffered':['微软 · 使用缓冲 I/O',                 K + 'using-buffered-i-o', '实操'],
 'neither': ['微软 · 使用 Neither I/O(直接给用户地址)', K + 'using-neither-buffered-nor-direct-i-o', '延伸'],
 'iocreate':['微软 · IoCreateDevice',               DDI + 'wdm/nf-wdm-iocreatedevice', '原文'],
 'iodel':   ['微软 · IoDeleteDevice',               DDI + 'wdm/nf-wdm-iodeletedevice', '原文'],
 'iosym':   ['微软 · IoCreateSymbolicLink',         DDI + 'wdm/nf-wdm-iocreatesymboliclink', '原文'],
 'iodelsym':['微软 · IoDeleteSymbolicLink',         DDI + 'wdm/nf-wdm-iodeletesymboliclink', '原文'],
 'iodevptr':['微软 · IoGetDeviceObjectPointer',     DDI + 'wdm/nf-wdm-iogetdeviceobjectpointer', '原文'],
 # 调试 / 蓝屏 / PE
 'dbgprint':['微软 · DbgPrint 内核调试输出',        DDI + 'wdm/nf-wdm-dbgprint', '原文'],
 'anadump': ['微软 · 用 WinDbg 分析内核转储',       DBG + 'analyzing-a-kernel-mode-dump-file-with-windbg', '实操'],
 'bugref':  ['微软 · Bug Check 蓝屏码参考',         DBG + 'bug-check-code-reference2', '延伸'],
 'pe':      ['微软 · PE 文件格式详解',              PE, '原文'],
 # WinDbg 命令(实操)
 'w_go':    ['WinDbg · 内核调试入门',   DBG + 'getting-started-with-windbg--kernel-mode-', '实操'],
 'w_lm':    ['WinDbg · lm 列出已加载模块', DBG + 'lm--list-loaded-modules-', '实操'],
 'w_drvobj':['WinDbg · !drvobj 看驱动对象', DBG + '-drvobj', '实操'],
 'w_devobj':['WinDbg · !devobj 看设备对象', DBG + '-devobj', '实操'],
 'w_object':['WinDbg · !object 看对象目录', DBG + '-object', '实操'],
 'w_analyze':['WinDbg · !analyze 自动分析蓝屏', DBG + '-analyze', '实操'],
 'w_dt':    ['WinDbg · dt 显示结构体',  DBG + 'dt--display-type-', '实操'],
 'w_s':     ['WinDbg · s 搜索内存(特征码)', DBG + 's--search-memory-', '实操'],
 'w_ln':    ['WinDbg · ln 查最近符号',  DBG + 'ln--list-nearest-symbols-', '实操'],
 'w_bp':    ['WinDbg · bp 下断点',      DBG + 'bp--bu--bm--set-breakpoint-', '实操'],
 'w_dds':   ['WinDbg · dds 显示内存并解析符号', DBG + 'dds--dps--dqs--display-words-and-symbols-', '实操'],
 'w_pool':  ['WinDbg · !poolused 看池占用', DBG + '-poolused', '实操'],
 # 博客园(中文主学 / 延伸)
 'cn_env':  ['博客园 · 驱动开发环境搭建',        CN + 'TechNomad/p/17443087.html', '主学'],
 'cn_intro':['博客园 · Windows 驱动开发入门指引', CN + 'liaoguifa/p/9049859.html', '主学'],
 'cn_vars': ['博客园 · Windows 内核重要全局变量', CN + 'xuanyuan/p/4165232.html', '主学'],
 'cn_enum': ['博客园 · 内核遍历驱动模块源码分析', CN + 'kuangke/p/6155360.html', '主学'],
 'cn_dkom': ['博客园 · lyshark · DKOM 直接内核对象操作隐藏', CN + 'LyShark/p/11652019.html', '主学'],
 'cn_comm': ['博客园 · 应用与驱动通信 DeviceIoControl', CN + 'lsh123/p/7354573.html', '主学'],
 'cn_irp':  ['博客园 · iBinary · 64 位内核 IRP 派遣函数与通信', CN + 'iBinary/p/15838812.html', '主学'],
 'cn_disp': ['博客园 · 《驱动开发技术详解》派遣函数', CN + 'predator-wang/p/5530392.html', '延伸'],
}

# ── 28 节:(导读一句话, 资料 key 列表) 按原顺序,索引即 data-id 序号 ──
L = [
 # U1 驱动基础与环境(0-6)
 ('内核开发不是"权限更高的应用编程"——地址空间共享、一崩就蓝屏、没有标准 C 运行库。第一步先把 VS + WDK + 虚拟机双机调试环境搭好,后面每节都在这套环境里跑。',
  ['cn_env', 'wdk', 'gs_tmpl']),
 ('一个驱动的骨架:DriverEntry(入口)+ DriverUnload(卸载)+ 派遣函数表。DRIVER_OBJECT 是系统交给你的"名片",所有回调都挂在它上面。先把这张图刻进脑子。',
  ['wdm', 'entry', 'drvobj']),
 ('驱动没有 printf——调试全靠 DbgPrint 把字符串送到内核调试器,或蓝屏/断点时 WinDbg 从另一台机器接管。理解双机内核调试的原理,才知道断点为什么能断在别人的内核里。',
  ['w_go', 'dbgprint', 'cn_intro']),
 ('驱动不是双击运行的——要通过服务控制管理器(创建 kernel 类型服务再 StartService)或 ZwLoadDriver 把 .sys 装进内核。测试阶段常用 sc / OSRLOADER,加载后用 lm 确认它真的在内核里了。',
  ['gs_start', 'gs_tmpl', 'w_lm']),
 ('驱动里一个空指针就是一次蓝屏。蓝屏不是"报错"而是内核主动停机自保——!analyze -v 会告诉你 bugcheck 码、出错模块和栈。学会读它,调试效率翻倍。',
  ['w_analyze', 'anadump', 'bugref']),
 ('把内核编程和应用编程的差异一次性梳理清楚:IRQL(中断请求级)、分页/非分页内存、无异常展开、调用约定、必须自己清理一切资源。这些是后面所有代码的隐形前提。',
  ['gs_all', 'wdm', 'ntzw']),
 ('内核函数分导出和未导出两类:导出的直接调,未导出的用 MmGetSystemRoutineAddress 按名字动态取址。Nt 与 Zw 前缀的区别(前置模式检查)也在这里搞清。',
  ['mmsys', 'ntzw', 'cn_vars']),
 # U2 内核编程常用设施(7-11)
 ('内核没有 malloc——用 ExAllocatePool2 从分页池或非分页池要内存,ExFreePool 还。高 IRQL 下只能碰非分页池,否则缺页直接蓝屏。配 RtlCopyMemory/RtlZeroMemory 做搬运和清零。',
  ['allocsp', 'expool2', 'rtlcopy']),
 ('内核字符串是带长度的 UNICODE_STRING,不以 \\0 结尾,不能用 strcmp。用 RtlInitUnicodeString 初始化、Rtl 系列做 Unicode↔ANSI 转换。搞错长度字段是新手最常见的越界源。',
  ['ustr', 'rtlinit', 'rtlu2a']),
 ('LIST_ENTRY 只有 Flink/Blink 两个指针,内核用它把进程、线程、模块全串成双向循环链表。关键是 CONTAINING_RECORD 宏——从链表节点用字段偏移反算出宿主结构首地址。',
  ['list', 'listhd', 'insert']),
 ('驱动加载后住在内核地址空间,有自己的模块基址和映像大小。PsLoadedModuleList 这个全局链表把所有内核模块串起来——它既是"查模块"的入口,也是下一单元"藏模块"的战场。',
  ['cn_vars', 'cn_enum', 'w_lm']),
 ('沿 PsLoadedModuleList 走 KLDR_DATA_TABLE_ENTRY 双链,就能枚举出全部已加载驱动的名字与基址。这是最基础的内核信息收集,也是特征搜索定位模块的前置。',
  ['cn_enum', 'list', 'w_lm']),
 # U3 驱动隐藏(12-14)
 ('DKOM 断链隐藏:把自己的 KLDR_DATA_TABLE_ENTRY 从 PsLoadedModuleList 里摘掉,lm 就看不到了。但要懂它的边界——\\Driver 目录、PatchGuard、内存扫描仍能发现你。',
  ['cn_dkom', 'cn_enum', 'w_lm']),
 ('更进一步:抹掉内存映像里的 MZ/PE 头、.pdb 路径等特征字符串,让扫描器难以识别。代码已加载进内存照常运行,抹的是"指纹"不是"身体"。',
  ['cn_dkom', 'pe', 'w_s']),
 ('反向操作:给一个设备对象,怎么回溯到它属于哪个驱动?DEVICE_OBJECT.DriverObject 一步到位,或用 IoGetDeviceObjectPointer 按名字拿设备栈,!drvobj/!devobj 在调试器里验证。',
  ['iodevptr', 'w_drvobj', 'w_object']),
 # U4 驱动通信(15-22)
 ('R3 和 R0 通信的三件套:命名设备对象(端点)+ 符号链接(让 R3 看得见)+ IRP(承载请求)。一次 DeviceIoControl 的完整旅程从这里开始,先建立整体流程图。',
  ['cn_comm', 'irp', 'access']),
 ('用 IoCreateDevice 建一个命名设备对象,作为 R3 打开的通信端点。设备名走 \\Device\\ 命名空间,只有内核看得见——所以还需要下一步的符号链接。',
  ['named', 'crdev', 'iocreate']),
 ('三种数据交互方式:缓冲 I/O(SystemBuffer 由内核代拷,最安全)、直接 I/O(MDL 锁页)、Neither(直接给你 R3 地址,最快也最危险)。METHOD_* 决定缓冲区从哪来。',
  ['access', 'buffered', 'ioctlbuf']),
 ('IoCreateSymbolicLink 把 \\Device\\xxx 映射成 R3 能 CreateFile 打开的 \\\\.\\xxx。没有它,应用层根本看不到你的设备。卸载时记得 IoDeleteSymbolicLink 配对删除。',
  ['iosym', 'named', 'iodelsym']),
 ('把处理函数填进 DriverObject->MajorFunction[] 数组:IRP_MJ_CREATE/CLOSE 让 CreateFile 能开关设备,IRP_MJ_DEVICE_CONTROL 收 IOCTL。没设 CREATE,R3 连打开都失败。',
  ['disp', 'irpmj', 'entry']),
 ('派遣函数内部:IoGetCurrentIrpStackLocation 取当前栈单元,读出 IoControlCode 和缓冲区长度,处理完必须 IoCompleteRequest 完成 IRP——忘了它,调用线程会永久卡死。',
  ['iostk', 'complete', 'cn_irp']),
 ('用 CTL_CODE 宏定义一个控制码(设备类型+功能号+传输方式+权限),R3 DeviceIoControl 发、R0 派遣函数收,一收一发跑通完整数据交互模板。',
  ['ioctldef', 'cn_comm', 'buffered']),
 ('把上面的零件封装成可复用的内核读写框架:一个 IOCTL 读、一个 IOCTL 写,统一处理缓冲区与错误码。后续读写别人进程内存、改内核数据都基于这个骨架。',
  ['access', 'rtlcopy', 'cn_irp']),
 # U5 特征搜索与安全攻防(23-27)
 ('特征码搜索:在内存里按一串标志性字节定位一个函数或数据——当目标符号未导出、地址随版本变时,这是唯一稳定的定位手段。先理解原理与它在攻防里的位置。',
  ['w_s', 'pe', 'cn_enum']),
 ('搜之前先划范围:拿到目标模块的基址和映像大小(走 PsLoadedModuleList,或 MmGetSystemRoutineAddress 反推)。全内核乱扫又慢又容易误报。',
  ['cn_enum', 'w_lm', 'mmsys']),
 ('再缩一层:解析 PE 节表,只在 .text 代码节里搜。数据节、重定位区里的巧合字节是误报的主要来源,按节区属性过滤能大幅提准。',
  ['pe', 'w_dt', 'cn_enum']),
 ('固定字节特征跨版本会失效——引入通配符(如 48 8B ?? ?? E8),把会随版本变的立即数/相对偏移用 ?? 跳过,只锚定稳定的 opcode 骨架。这是特征选取的核心技巧。',
  ['w_s', 'pe', 'cn_dkom']),
 ('最后把"定位模块 → 枚举节区 → 模糊匹配"封装成一个通用特征搜索引擎:输入模块名+带通配的特征串,输出唯一命中地址。这是内核攻防工具的地基。',
  ['cn_enum', 'w_s', 'pe']),
]

UNITS = [
 (0, 7,   '第一单元 · 驱动基础与调试环境'),
 (7, 12,  '第二单元 · 内核编程常用设施(内存 · 字符串 · 链表 · 模块)'),
 (12, 15, '第三单元 · 驱动隐藏与对象回溯'),
 (15, 23, '第四单元 · 驱动通信(设备对象 · 符号链接 · IRP · IOCTL)'),
 (23, 28, '第五单元 · 特征搜索与安全攻防'),
]

GATES = [
 {
  'title': '驱动基础与调试环境',
  'quiz': [
   {'q': '内核态开发和用户态开发最根本的几个差异是什么(至少说三条)?',
    'a': '① 所有驱动共享同一内核地址空间,一个越界就影响全局;② 任何未处理异常都是蓝屏(整机停机),没有"这个进程崩了重启就好";③ 没有标准 C 运行库(malloc/printf 都用不了),要用 Ex/Rtl 系列;④ 有 IRQL 概念,高 IRQL 下能做的事受限;⑤ 资源(内存/对象/符号链接)必须自己在 Unload 里全部清理。'},
   {'q': 'DriverEntry 的两个参数是什么?一个可加载的驱动最少要做哪几件事?',
    'a': '参数是 PDRIVER_OBJECT DriverObject 和 PUNICODE_STRING RegistryPath。最少要:设置 DriverObject->DriverUnload(否则驱动无法卸载);按需填 MajorFunction 派遣表;若要通信则 IoCreateDevice + IoCreateSymbolicLink;返回 STATUS_SUCCESS。'},
   {'q': '为什么驱动实验要在虚拟机 + 双机内核调试里做?测试机还需要什么前置设置?',
    'a': '因为蓝屏会整机停机,虚拟机可随时回滚快照且不损坏宿主;双机调试让 WinDbg 能在断点或蓝屏瞬间从另一端接管。测试机需开启测试签名模式(bcdedit /set testsigning on)和调试(/debug on),否则未签名驱动加载会失败(错误 1275)。'},
   {'q': '`!analyze -v` 在蓝屏后给你哪四类关键信息?',
    'a': 'Bug Check 码及其参数(定位崩溃类别)、出错的模块/驱动名(IMAGE_NAME)、失败指令附近的反汇编、以及崩溃点的调用栈(STACK_TEXT)。'},
  ],
  'lab': {
   'task': '写一个最小驱动:DriverEntry 里 DbgPrint 一行、注册 DriverUnload 也打印一行;编译后加载,看到输出,再卸载。',
   'steps': [
    '用 WDK 模板建一个空 KMDF/WDM 驱动工程,DriverEntry 里 DbgPrint("Hello from %wZ\\n", RegistryPath); 并设 DriverObject->DriverUnload。',
    '测试机 bcdedit /set testsigning on 后重启;用 sc create MyDrv type= kernel binPath= <路径> 建服务。',
    'sc start MyDrv 加载;在 WinDbg 或 DebugView 里确认看到 DriverEntry 的打印。',
    'lm m MyDrv 确认模块已在内核;记下它的基址。',
    'sc stop MyDrv 卸载,确认看到 Unload 打印且 lm 里模块消失。',
   ],
   'pass': '加载/卸载各看到一行打印;lm 能看到又能看到它消失;并能说清楚"为什么没设 DriverUnload 就卸不掉"。',
   'tip': '看不到 DbgPrint 时先设过滤掩码:注册表 HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Debug Print Filter 下 DEFAULT=0xFFFFFFFF,或 WinDbg 里 ed nt!Kd_DEFAULT_Mask 0xF。',
  },
  'pits': [
   {'s': 'sc start 报错 1275 "此驱动程序已被阻止加载"', 'c': '未开测试签名模式,或驱动未签名/系统开了强制签名。',
    'f': 'bcdedit /set testsigning on 并重启;确认是 64 位系统的测试模式生效(桌面右下角有水印)。'},
   {'s': 'DbgPrint 完全看不到输出', 'c': 'Debug Print Filter 掩码默认屏蔽了 DPFLTR_DEFAULT。',
    'f': '设掩码(见 tip);或用 DbgPrintEx 指定分量,并确认 WinDbg 已连上目标机。'},
   {'s': 'sc stop 后驱动卸不掉 / 停不了', 'c': '没有设置 DriverUnload 例程。',
    'f': 'DriverEntry 里务必 DriverObject->DriverUnload = MyUnload;,并在其中删掉设备对象和符号链接。'},
  ],
 },
 {
  'title': '内核编程常用设施',
  'quiz': [
   {'q': 'ExAllocatePool2 相比老的 ExAllocatePoolWithTag 有哪些改进?为什么内存要带 Tag?',
    'a': 'ExAllocatePool2 默认清零、用 POOL_FLAGS 显式表达意图、对齐更规范,是现代推荐接口。Tag(四字节)让你能用 !poolused / !pool 按标记统计和排查泄漏,定位是谁分配没释放。'},
   {'q': '分页池和非分页池的区别是什么?什么情况下必须用非分页池?',
    'a': '分页池的内存可被换出到磁盘,只能在低 IRQL(< DISPATCH_LEVEL)访问;非分页池常驻物理内存。凡是会在 DISPATCH_LEVEL 及以上访问的数据(如 DPC、ISR、持锁期间用到的结构)必须放非分页池,否则触发不可换页的缺页 → 蓝屏。'},
   {'q': '为什么内核里不能用 strcmp 比较驱动名或路径?正确做法是什么?',
    'a': '内核字符串是 UNICODE_STRING:{Length, MaximumLength, Buffer},按 Length 计长、不保证以 \\0 结尾,直接当 C 字符串处理会越界或截断。要用 RtlEqualUnicodeString / RtlCompareUnicodeString 等 Rtl 系列。'},
   {'q': 'LIST_ENTRY 节点里只有 Flink/Blink,怎么从遍历到的节点拿到它所在的宿主结构?',
    'a': '用 CONTAINING_RECORD(address, type, field):已知某字段的地址、宿主类型、字段名,宏用"字段在结构里的偏移"反算出结构首地址。内核遍历 EPROCESS/模块链全靠它。'},
  ],
  'lab': {
   'task': '分配一块带 Tag 的非分页池,清零后写入数据,在调试器里按 Tag 找到它,再正确释放;然后故意漏释放,观察后果。',
   'steps': [
    "用 ExAllocatePool2(POOL_FLAG_NON_PAGED, size, 'tseT') 分配(注意 Tag 是四字符)。",
    'RtlZeroMemory 清零后 RtlCopyMemory 写入一段可辨认的数据。',
    "WinDbg 里 !poolused 2 找到你的 Tag(注意字节序,'tseT' 显示为 Test);或 !pool <地址> 看这块的 Tag 与大小。",
    'ExFreePool 释放;再 !poolused 确认它消失。',
    '改代码故意不释放就卸载驱动,开 Driver Verifier 勾选 Pool Tracking,观察它报出泄漏。',
   ],
   'pass': '!poolused 能按 Tag 定位到你的分配,释放后消失;并能解释漏释放为什么会被 Verifier 抓到。',
   'tip': "Tag 常写成四个字符的字符串,内核里以小端存放,所以 'Test' 在 !poolused 里可能显示为 'tseT'——查的时候注意反过来。",
  },
  'pits': [
   {'s': '在 DISPATCH_LEVEL 访问刚分配的内存就蓝屏(IRQL_NOT_LESS_OR_EQUAL)', 'c': '把数据放进了分页池,高 IRQL 下被换出触发缺页。',
    'f': '改用 POOL_FLAG_NON_PAGED;凡是可能在高 IRQL 碰的数据一律非分页。'},
   {'s': '释放后系统随机蓝屏(BAD_POOL_CALLER / DOUBLE_FREE)', 'c': '重复释放同一块,或释放了非池指针/越界写坏了池头。',
    'f': '释放后立刻把指针置 NULL;写入严格不超过分配长度;用 Verifier 的特殊池定位越界。'},
   {'s': 'UNICODE_STRING 比较/拷贝时数据被截断', 'c': '按 \\0 结尾处理了,或没同步更新 Length 字段。',
    'f': '一律用 Rtl 系列并以 Length 为准;自己填 Buffer 后手动设置正确的 Length。'},
  ],
 },
 {
  'title': '驱动隐藏与对象回溯',
  'quiz': [
   {'q': 'DKOM 断链隐藏改的是哪个链表?断链后 lm 还看得到吗?为什么有些工具仍能发现被隐藏的驱动?',
    'a': '改 PsLoadedModuleList 上 KLDR_DATA_TABLE_ENTRY 的 InLoadOrderLinks(把自己的前后指针互相接上、跳过自己)。断链后基于该链表的 lm 看不到;但 \\Driver 对象目录、句柄表、PatchGuard 完整性校验、以及直接扫描内存里的 PE 特征都能另辟蹊径发现它。'},
   {'q': '断链操作为什么必须保证原子性(加锁 / 关中断 / 保证不被打断)?',
    'a': '链表是多核共享的,断链要同时改前节点的 Flink 和后节点的 Blink 两处。若中途被另一个核的遍历或插入打断,链表处于不一致状态,会导致遍历越界 → 蓝屏。'},
   {'q': '抹除 PE 头之后驱动还能运行吗?抹的是文件里的头还是内存里的头?目的是什么?',
    'a': '照常运行——代码和数据已经加载并重定位完成,MZ/PE 头只是加载期用的元数据。抹的是内存映像里的头(以及 .pdb 路径等字符串),目的是让"扫描内存找 PE 特征"的检测工具认不出这块内存是一个模块。'},
   {'q': '给定一个 DEVICE_OBJECT,如何回溯到它属于哪个驱动?',
    'a': '直接读 DEVICE_OBJECT->DriverObject 就是所属驱动对象;调试器里 !devobj <设备> 看它、!drvobj <驱动> 看该驱动的设备栈与派遣函数表。程序里也可用 IoGetDeviceObjectPointer 按设备名拿到设备对象再回溯。'},
  ],
  'lab': {
   'task': '在 WinDbg 里手动沿模块链走几步读出模块名,再对一个驱动 !drvobj 看它的派遣表——把"遍历"和"回溯"都亲手做一遍。',
   'steps': [
    'dt nt!_KLDR_DATA_TABLE_ENTRY 看清 InLoadOrderLinks / DllBase / FullDllName 各字段偏移。',
    'x nt!PsLoadedModuleList 取链表头地址;dt nt!_KLDR_DATA_TABLE_ENTRY <某模块表项> 展开一项。',
    '顺着 InLoadOrderLinks.Flink 走 2~3 步(记得减去字段偏移得到结构首地址),每步打印 FullDllName,对照 lm 的输出。',
    '挑一个驱动 !drvobj <驱动名> 2 看它的设备对象和 MajorFunction 表;再 !devobj <设备地址> 反查 DriverObject。',
    '(选做)理解:如果把某项的 Flink/Blink 互相接上跳过它,lm 会怎样。',
   ],
   'pass': '能手动遍历模块链并读出正确的模块名;能从一个设备对象回溯到它的 DriverObject 并看到派遣表。',
   'tip': 'x64 与 x86 下 _KLDR_DATA_TABLE_ENTRY 字段偏移不同,务必用 dt 让符号告诉你偏移,别硬编码。',
  },
  'pits': [
   {'s': '改动模块链或 PE 头后系统隔一会儿就蓝屏(通常是 CRITICAL_STRUCTURE_CORRUPTION)', 'c': 'PatchGuard 检测到关键内核结构被篡改。',
    'f': '这类实验只在关闭/不含 PG 的测试环境或旧系统的虚拟机里做,并理解 PG 保护的范围。'},
   {'s': '手动遍历时读出的模块名是乱码或地址无效', 'c': '忘了从链表节点地址减去 InLoadOrderLinks 的字段偏移,直接把 Flink 当结构首地址用了。',
    'f': '结构首地址 = 节点地址 - InLoadOrderLinks 偏移(即 CONTAINING_RECORD 的道理)。'},
   {'s': '断链后多核机器偶发崩溃', 'c': '只在一个核视角改了链表,或改的过程被并发遍历打断。',
    'f': '断链要原子完成;理解链表是全局共享的,任何时刻都可能有别的核在遍历。'},
  ],
 },
 {
  'title': '驱动通信全链路',
  'quiz': [
   {'q': 'R3 一次 DeviceIoControl,IO 管理器生成的 IRP 的 MajorFunction 是什么?派遣函数从哪里取控制码和缓冲区长度?',
    'a': 'IRP_MJ_DEVICE_CONTROL。用 IoGetCurrentIrpStackLocation(Irp) 拿当前栈单元,从 Parameters.DeviceIoControl 里取 IoControlCode、InputBufferLength、OutputBufferLength。'},
   {'q': 'METHOD_BUFFERED / METHOD_IN_DIRECT / METHOD_OUT_DIRECT / METHOD_NEITHER 四种方式,输入输出缓冲区分别从哪里拿?哪种最危险?',
    'a': 'BUFFERED:输入输出都走 Irp->AssociatedIrp.SystemBuffer(内核代拷,最安全)。IN/OUT_DIRECT:输入走 SystemBuffer,输出/输入的大块走 MDL(Irp->MdlAddress)锁页映射。NEITHER:直接给你 R3 的虚拟地址(Type3InputBuffer / UserBuffer),最快也最危险——必须 ProbeForRead/Write + try/except,否则 R3 传个坏地址就蓝屏。'},
   {'q': '为什么必须创建符号链接?R3 能直接用 \\Device\\xxx 去 CreateFile 吗?',
    'a': '不能。\\Device\\ 在内核对象命名空间,R3 的 Win32 命名空间看不到。要用 IoCreateSymbolicLink 在 \\DosDevices(\\??)下建符号链接,R3 才能用 \\\\.\\xxx 打开。'},
   {'q': '派遣函数处理完 IRP 却忘了 IoCompleteRequest 会发生什么?',
    'a': '该 IRP 永远处于未完成状态,发起调用的 R3 线程会一直阻塞在 DeviceIoControl 里(除非驱动被强制卸载)。凡是你不 pending 的 IRP,处理完都必须设置 IoStatus 并 IoCompleteRequest。'},
  ],
  'lab': {
   'task': '写一个能收发数据的驱动:R3 用 CreateFile 打开符号链接,DeviceIoControl 发一串字节,驱动改写后回传;在派遣函数下断点看控制码。',
   'steps': [
    '驱动:IoCreateDevice 建 \\Device\\MyComm,IoCreateSymbolicLink 到 \\DosDevices\\MyComm;填 IRP_MJ_CREATE/CLOSE/DEVICE_CONTROL 派遣。',
    "用 CTL_CODE(FILE_DEVICE_UNKNOWN, 0x800, METHOD_BUFFERED, FILE_ANY_ACCESS) 定义一个 IOCTL。",
    'DEVICE_CONTROL 派遣里:IoGetCurrentIrpStackLocation 取 IoControlCode,从 SystemBuffer 读入、改写、写回,设 Irp->IoStatus.Information = 回传长度,IoCompleteRequest。',
    'R3:CreateFile("\\\\\\\\.\\\\MyComm", ...) 打开,DeviceIoControl 发送 buffer 并接收回写。',
    'WinDbg 里 bp <你的DEVICE_CONTROL派遣函数>,命中后 dt nt!_IO_STACK_LOCATION <栈单元> 看 IoControlCode 和长度。',
   ],
   'pass': 'R3 收到驱动回写后的数据;断点处能读出正确的 IoControlCode 与 InputBufferLength;IRP 被正确完成、R3 不卡死。',
   'tip': 'C 字符串里 \\\\.\\MyComm 要写成 "\\\\\\\\.\\\\MyComm";METHOD_BUFFERED 下输入输出复用同一个 SystemBuffer,先读完输入再写输出。',
  },
  'pits': [
   {'s': 'R3 CreateFile 直接失败(GetLastError 2 或 5)', 'c': '符号链接没建/名字不匹配,或没设 IRP_MJ_CREATE 派遣。',
    'f': '确认 IoCreateSymbolicLink 成功、R3 路径与之对应、CREATE/CLOSE 派遣都填了(哪怕只是完成 IRP 返回成功)。'},
   {'s': 'METHOD_NEITHER 下一解引用缓冲区就蓝屏', 'c': '直接用了 R3 传来的原始地址,没有校验。',
    'f': '进 try/except 用 ProbeForRead/ProbeForWrite 校验,或干脆改用 METHOD_BUFFERED 让内核代拷。'},
   {'s': 'R3 读到的输出是空的或旧数据', 'c': '忘了设 Irp->IoStatus.Information 为实际写回字节数。',
    'f': 'Information 必须等于你写进 SystemBuffer 的输出长度,R3 的 lpBytesReturned 才对。'},
  ],
 },
 {
  'title': '特征搜索引擎',
  'quiz': [
   {'q': '为什么特征搜索要先定位模块基址、再只搜 .text 节,而不是直接全内核扫?',
    'a': '① 缩小范围大幅提速;② 数据节/重定位区/只读常量里会有和特征串巧合的字节,限定在稳定的 .text 代码节能显著降低误报;③ 全内核扫还可能碰到分页换出或无效区间导致异常。'},
   {'q': '模糊匹配的通配符(如 48 8B ?? ?? E8 中的 ??)解决什么问题?',
    'a': '跨版本/跨补丁时,指令里的立即数、相对偏移、被重定位的地址会变,但 opcode 骨架通常不变。用 ?? 跳过这些易变字节,只锚定稳定部分,让同一条特征在不同版本上都能命中。'},
   {'q': '选取特征字节时要避开哪些内容,才不会换一台机器 / 换一个版本就失效?',
    'a': '避开会被重定位的绝对地址、call/jmp 的相对偏移、随版本变化的立即数常量;优先选连续且稳定的 opcode + ModRM 骨架,并保证这段在目标范围内唯一。'},
   {'q': 'PE 的哪个结构描述各节区的 RVA、大小和属性?怎么遍历到它们?',
    'a': 'IMAGE_SECTION_HEADER 数组,每项含 VirtualAddress(RVA)、Misc.VirtualSize、Characteristics(可执行/可写等)。从 IMAGE_DOS_HEADER→IMAGE_NT_HEADERS,按 FileHeader.NumberOfSections 遍历紧随可选头之后的节表。'},
  ],
  'lab': {
   'task': '在 WinDbg 里对 nt 模块,拿基址→定位 .text 范围→在范围内搜一段你选定的字节特征,用 ln 确认命中的是目标函数。',
   'steps': [
    'lm m nt 拿到 nt 的基址和结束地址。',
    '!dh <nt基址> 或 dt 解析 PE,找到 .text 节的起始 RVA 和大小,算出 [起始, 结束] 虚拟地址范围。',
    '挑一个已知函数(如 nt!NtCreateFile),u 反汇编取它开头一段稳定字节作为特征。',
    's -b <.text起始> <.text结束> <你的特征字节> 在范围内搜索。',
    'ln <命中地址> 确认它就是目标函数;若命中多处,说明特征不唯一,回去加长或换更独特的片段。',
   ],
   'pass': 's 在 .text 范围内唯一命中你的目标函数,ln 对上;并能说清楚所选特征里哪些字节稳定、哪些应该换成通配。',
   'tip': 's -b 是按字节搜;把范围严格限定在 .text 内能避免命中数据节的巧合字节。命中过多就加长特征或挑更独特的指令序列。',
  },
  'pits': [
   {'s': 's 在模块里搜到多个命中,无法确定目标', 'c': '特征太短/太常见,或没限定在 .text 范围内。',
    'f': '加长特征、挑更独特的指令序列,并把搜索范围严格限制在代码节。'},
   {'s': '特征在本机好用,换一台机器 / 打了补丁就搜不到', 'c': '把会随版本变化的立即数或重定位地址选进了特征。',
    'f': '把这些易变字节改成通配 ??,只保留稳定的 opcode 骨架;必要时准备多套特征做回退。'},
   {'s': '手算 .text 范围时越界或读到无效内存', 'c': 'RVA 没加模块基址,或 x64 下把地址位宽/节头偏移算错。',
    'f': '虚拟地址 = 模块基址 + 节的 VirtualAddress;用 !dh/dt 让工具报节表,别手撸偏移。'},
  ],
 },
]

src = json.load(open(r'C:\learning\windbg-driver-roadmap\build\course_14.json', encoding='utf-8'))
titles = src['chapters'][0]['lessons']
assert len(titles) == 28 and all(isinstance(t, str) for t in titles), '课程结构变了,请检查'
assert len(L) == 28, 'L 应有 28 项'

chapters = []
for (a, b, name), gate in zip(UNITS, GATES):
    lessons = []
    for i in range(a, b):
        w, keys = L[i]
        lessons.append({'t': titles[i], 'w': w, 'r': [R[k] for k in keys]})
    chapters.append({'title': name, 'lessons': lessons, 'gate': gate})

src['chapters'] = chapters
with open(r'C:\learning\windbg-driver-roadmap\build\course_14.json', 'w',
          encoding='utf-8', newline='\n') as f:
    json.dump(src, f, ensure_ascii=False, indent=2)
    f.write('\n')

n = sum(len(c['lessons']) for c in chapters)
print('course_14: %d 单元 / %d 节,全部带导读+资料;%d 个验收关卡' % (len(chapters), n, len(GATES)))
