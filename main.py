import os,sys,shutil,tempfile,subprocess,threading,tkinter as tk
from tkinter import ttk,messagebox
import psutil

def resource_path(relative):
 base=getattr(sys,"_MEIPASS",os.path.dirname(os.path.abspath(__file__)))
 return os.path.join(base,relative)

def set_window_icon(root):
 try:root.iconbitmap(resource_path(os.path.join("assets","feather-logo.ico")))
 except Exception:pass
BG="#000000"; P="#111111"; FG="#eeeeee"; M="#999999"
TXT={"en":{"dash":"DASHBOARD","apps":"APP BOOSTER","clean":"DISK CLEANER","settings":"SETTINGS","music":"MUSIC PLAYER","cpu":"CPU","ram":"RAM","disk":"DISK","refresh":"REFRESH","choose":"Choose a running process","boost":"SET ABOVE NORMAL","optimize":"SMART OPTIMIZE","uninstall":"UNINSTALL APPS","cleanbtn":"CLEAN TEMP FILES","restore":"CREATE RESTORE POINT","startup":"ENABLE STARTUP SCAN","manual":"MANUAL MODE — changes need your action","warning":"Conservative tools. No Windows services disabled; Realtime priority is excluded.","drivers":"OFFLINE DRIVERS","drvsub":"Scan the bundled Drivers folder and install matching INF packages offline.","drvchoose":"SELECT DRIVER FOLDER","drvinstall":"INSTALL SELECTED DRIVER","drvauto":"SCAN & INSTALL MATCHING DRIVERS","drvempty":"No INF driver files found in this folder.","drvselect":"Select an INF driver first.","drvconfirm":"Install this driver using Windows PnPUtil? Only install drivers intended for your Acer Aspire 5336.","drvok":"Windows accepted the driver installation command. Restart may be required.","drvfail":"Driver installation failed. Run as Administrator and verify driver compatibility.","drvfolder":"Driver folder: {}","drvbackup":"BACK UP INSTALLED DRIVERS","lang":"العربية","ask":"Delete temporary files? Files in use are skipped.","done":"Deleted {} files; skipped {}.","askrp":"Request a Windows restore point? Admin rights/System Protection may be required.","rpok":"Restore point command completed.","rpfail":"Restore point failed. Run as Administrator and check System Protection.","noapp":"Select a process first.","boostok":"Priority set to Above Normal.","boostfail":"Could not change priority."},"ar":{"dash":"لوحة التحكم","apps":"معزز التطبيقات","clean":"تنظيف الملفات","settings":"الإعدادات","music":"مشغل الموسيقى","cpu":"المعالج","ram":"الذاكرة","disk":"القرص","refresh":"تحديث","choose":"اختر عملية قيد التشغيل","boost":"تعيين أولوية أعلى من العادية","optimize":"التحسين الذكي","uninstall":"إزالة التطبيقات","cleanbtn":"تنظيف الملفات المؤقتة","restore":"إنشاء نقطة استعادة","startup":"تفعيل فحص بدء التشغيل","manual":"الوضع اليدوي — التغييرات بموافقتك","warning":"أدوات محافظة. لا نعطّل خدمات ويندوز ولا نستخدم أولوية الوقت الحقيقي.","drivers":"التعريفات بدون إنترنت","drvsub":"فحص مجلد Drivers المرفق وتثبيت ملفات INF المطابقة دون إنترنت.","drvchoose":"اختيار مجلد التعريفات","drvinstall":"تثبيت التعريف المحدد","drvauto":"فحص وتثبيت التعريفات المتطابقة","drvempty":"لم يتم العثور على ملفات تعريف INF في هذا المجلد.","drvselect":"اختر ملف تعريف INF أولاً.","drvconfirm":"هل تريد تثبيت هذا التعريف باستخدام أداة ويندوز؟ ثبّت فقط تعريفاً مخصصاً لجهاز Acer Aspire 5336.","drvok":"قبل ويندوز أمر تثبيت التعريف. قد تحتاج إلى إعادة التشغيل.","drvfail":"فشل تثبيت التعريف. شغّل البرنامج كمسؤول وتأكد من توافق التعريف.","drvfolder":"مجلد التعريفات: {}","drvbackup":"نسخ احتياطي للتعريفات المثبتة","lang":"English","ask":"حذف الملفات المؤقتة؟ سيتم تخطي الملفات المستخدمة.","done":"تم حذف {} ملف وتخطي {}.","askrp":"طلب إنشاء نقطة استعادة؟ قد تحتاج صلاحيات المسؤول وحماية النظام.","rpok":"اكتمل أمر نقطة الاستعادة.","rpfail":"فشل إنشاء نقطة الاستعادة. شغّل كمسؤول وتحقق من حماية النظام.","noapp":"اختر عملية أولاً.","boostok":"تم تعيين الأولوية أعلى من العادية.","boostfail":"تعذر تغيير الأولوية."}}
class App:
 def __init__(s,r,lang="en"):
  s.r=r;s.l=lang;s.t=TXT[s.l];s.pid=None;r.title("OPTIMIZE WIN 10 v1.0");set_window_icon(r);r.geometry("950x650");r.configure(bg=BG);r.minsize(800,520)
  h=tk.Frame(r,bg="#0b0b0b",highlightbackground="#303030",highlightthickness=1);h.pack(fill="x",padx=20,pady=(16,12));logo=tk.Canvas(h,width=48,height=42,bg="#0b0b0b",highlightthickness=0);logo.pack(side="left",padx=(14,10),pady=8);logo.create_polygon(3,6,22,4,22,20,3,22,fill="#FFFFFF",outline="");logo.create_polygon(25,3,45,1,45,19,25,20,fill="#FFFFFF",outline="");logo.create_polygon(3,25,22,23,22,39,3,36,fill="#FFFFFF",outline="");logo.create_polygon(25,23,45,22,45,40,25,39,fill="#FFFFFF",outline="");brand=tk.Frame(h,bg="#0b0b0b");brand.pack(side="left",pady=7);tk.Label(brand,text="OPTIMIZE WIN 10  •  v1.0",bg="#080808",fg=FG,font=("Segoe UI",18,"bold")).pack(anchor="w");tk.Label(brand,text="SYSTEM PERFORMANCE CENTER",bg="#080808",fg="#888888",font=("Segoe UI",8,"bold")).pack(anchor="w")
  s.lb=s.btn(h,"العربية",s.toggle);s.lb.pack(side="right");s.md=tk.Label(h,text=s.t["manual"],bg=BG,fg=M);s.md.pack(side="right",padx=16)
  s.nav=tk.Frame(r,bg=BG);s.nav.pack(fill="x",padx=20);s.body=tk.Frame(r,bg=BG);s.body.pack(fill="both",expand=True,padx=20,pady=14)
  s.status=tk.StringVar(value="Ready");tk.Label(r,textvariable=s.status,bg="#080808",fg=M,anchor="w",padx=20,pady=8).pack(fill="x",side="bottom")
  s.nb=[]
  for k,f in [("dash",s.dashboard),("apps",s.apps),("clean",s.cleaner),("drivers",s.drivers),("music",s.music),("settings",s.settings)]:
   b=s.btn(s.nav,s.t[k],f);b.pack(side="left",padx=(0,8));s.nb.append((k,b))
  s.dashboard();s.tick()
  if "--startup-scan" in sys.argv:r.after(900,s.scan)
 def btn(s,p,t,f):return tk.Button(p,text=t,command=f,bg="#191919",fg=FG,activebackground="#333",activeforeground=FG,relief="flat",bd=0,padx=14,pady=9,font=("Segoe UI",9,"bold"))
 def clear(s):
  for w in s.body.winfo_children():w.destroy()
 def head(s,k,sub=""):
  tk.Label(s.body,text=s.t[k],bg=BG,fg=FG,font=("Segoe UI",18,"bold")).pack(anchor="w",pady=(0,8))
  if sub:tk.Label(s.body,text=sub,bg=BG,fg=M).pack(anchor="w",pady=(0,12))
 def tree(s,h=11):
  st=ttk.Style();st.theme_use("clam");st.configure("Treeview",background=P,foreground=FG,fieldbackground=P,rowheight=26);st.configure("Treeview.Heading",background="#202020",foreground=FG)
  t=ttk.Treeview(s.body,columns=("n","p","m"),show="headings",height=h)
  for c,n,w in [("n","Process",420),("p","PID",100),("m","Memory MB",130)]:t.heading(c,text=n);t.column(c,width=w)
  t.pack(fill="both",expand=True);t.bind("<<TreeviewSelect>>",lambda e:s.select(t));s.tr=t;s.refresh()
 def select(s,t):
  if t.selection():s.pid=int(t.item(t.selection()[0],"values")[1])
 def refresh(s):
  if not hasattr(s,"tr") or not s.tr.winfo_exists():return
  s.tr.delete(*s.tr.get_children());a=[]
  for p in psutil.process_iter(["pid","name","memory_info"]):
   try:a.append((p.info["name"] or "?",p.info["pid"],p.info["memory_info"].rss/1048576))
   except Exception:pass
  for n,p,m in sorted(a,key=lambda x:x[2],reverse=True)[:120]:s.tr.insert("","end",values=(n,p,f"{m:.1f}"))
 def dashboard(s):
  s.clear()
  top=tk.Frame(s.body,bg=BG);top.pack(fill="x")
  title=tk.Frame(top,bg=BG);title.pack(side="left",fill="x",expand=True)
  tk.Label(title,text=s.t["dash"],bg=BG,fg=FG,font=("Segoe UI",18,"bold")).pack(anchor="w")
  tk.Label(title,text=s.t["warning"],bg=BG,fg=M).pack(anchor="w",pady=(4,0))
  winlogo=tk.Canvas(top,width=62,height=54,bg=BG,highlightthickness=0);winlogo.pack(side="right",padx=8,pady=2)
  winlogo.create_polygon(3,7,29,4,29,25,3,27,fill="#FFFFFF",outline="")
  winlogo.create_polygon(33,3,59,0,59,23,33,25,fill="#FFFFFF",outline="")
  winlogo.create_polygon(3,31,29,29,29,51,3,47,fill="#FFFFFF",outline="")
  winlogo.create_polygon(33,29,59,26,59,52,33,51,fill="#FFFFFF",outline="")
  row=tk.Frame(s.body,bg=BG);row.pack(fill="x",pady=8);s.v={}
  for k in ("cpu","ram","disk"):
   f=tk.Frame(row,bg=P,padx=18,pady=14);f.pack(side="left",fill="both",expand=True,padx=(0,10));tk.Label(f,text=s.t[k],bg=P,fg=M).pack(anchor="w");v=tk.Label(f,text="--",bg=P,fg=FG,font=("Segoe UI",23,"bold"));v.pack(anchor="w",pady=8);s.v[k]=v
  actions=tk.Frame(s.body,bg=BG);actions.pack(fill="x",pady=(8,10))
  tk.Label(actions,text="QUICK OPTIMIZE",bg=BG,fg=FG,font=("Segoe UI",11,"bold")).pack(anchor="w",pady=(0,7))
  quick=tk.Frame(actions,bg=BG);quick.pack(fill="x")
  selfbtn=s.btn(quick,s.t["optimize"],s.optimize_now);selfbtn.pack(side="left",padx=(0,8))
  s.btn(quick,"APP BOOSTER",s.apps).pack(side="left",padx=(0,8))
  s.btn(quick,s.t["cleanbtn"],s.cleaner).pack(side="left",padx=(0,8))
  s.btn(quick,s.t["restore"],s.restore).pack(side="left",padx=(0,8))
  s.btn(quick,"DARK MODE / الوضع الداكن",s.toggle_windows_theme).pack(side="left",padx=(0,8))
  s.btn(quick,s.t["uninstall"],s.uninstall_apps).pack(side="left",padx=(0,8))
  s.btn(quick,s.t["drivers"],s.drivers).pack(side="left")
  s.btn(s.body,s.t["refresh"],s.refresh).pack(anchor="e",pady=5);s.tree(8)
 def tick(s):
  try:
   if hasattr(s,"v"):
    disk = psutil.disk_usage(os.environ.get("SystemDrive", "C:") + "\\").percent
    s.v["cpu"].config(text=f"{psutil.cpu_percent()}%");s.v["ram"].config(text=f"{psutil.virtual_memory().percent}%");s.v["disk"].config(text=f"{disk}%")
  except Exception:pass
  s.r.after(2500,s.tick)
 def apps(s):
  s.clear();s.head("apps",s.t["warning"]);tk.Label(s.body,text=s.t["choose"],bg=BG,fg=FG).pack(anchor="w");s.tree(11);row=tk.Frame(s.body,bg=BG);row.pack(fill="x",pady=10);s.btn(row,s.t["boost"],s.boost).pack(side="left",padx=(0,8));s.btn(row,s.t["uninstall"],s.uninstall_apps).pack(side="left")
 def optimize_now(s):
  s.clear()
  s.head("dash", "Choose a category. Every tool runs separately and asks before changing Windows." if s.l=="en" else "اختر قسماً. كل أداة مستقلة وتطلب موافقتك قبل تغيير ويندوز.")
  cards=[
   ("STORAGE / التخزين","Clean temp files, Recycle Bin and open Disk Cleanup",s.storage_tools),
   ("STARTUP / بدء التشغيل","Review apps that launch with Windows",s.startup_tools),
   ("MEMORY / الذاكرة","Monitor RAM and inspect high-memory processes",s.memory_tools),
   ("NETWORK / الشبكة","Flush DNS, inspect adapters and reset network stack",s.network_tools),
   ("PERFORMANCE / الأداء","Power mode, drive optimization and Game Mode",s.performance_tools),
   ("REPAIR / إصلاح النظام","Run Windows image and system-file checks",s.repair_tools),
   ("APPS / التطبيقات","Open installed-app management",s.uninstall_apps),
   ("RESTORE / الاستعادة","Create a restore point before system changes",s.restore),
  ]
  grid=tk.Frame(s.body,bg=BG);grid.pack(fill="both",expand=True)
  for i,(name,desc,action) in enumerate(cards):
   card=tk.Frame(grid,bg=P,padx=14,pady=12);card.grid(row=i//2,column=i%2,sticky="nsew",padx=6,pady=6)
   tk.Label(card,text=name,bg=P,fg=FG,font=("Segoe UI",11,"bold")).pack(anchor="w")
   tk.Label(card,text=desc,bg=P,fg=M,wraplength=340,justify="left").pack(anchor="w",pady=(5,10))
   s.btn(card,"OPEN / فتح",action).pack(anchor="w")
  grid.grid_columnconfigure(0,weight=1);grid.grid_columnconfigure(1,weight=1)
  grid.grid_rowconfigure(0,weight=1);grid.grid_rowconfigure(1,weight=1);grid.grid_rowconfigure(2,weight=1);grid.grid_rowconfigure(3,weight=1)
 def storage_tools(s):
  s.clear();s.head("clean","Select one storage task at a time." if s.l=="en" else "اختر مهمة تخزين واحدة في كل مرة.")
  s.btn(s.body,"CLEAN TEMP FILES / تنظيف الملفات المؤقتة",s.cleaner).pack(anchor="w",pady=6)
  def recycle():
   if not messagebox.askyesno("OPTIMIZE","Empty the Recycle Bin? This removes its contents."):return
   try:
    subprocess.run(["powershell.exe","-NoProfile","-Command","Clear-RecycleBin -Force -ErrorAction Stop"],check=True,timeout=120)
    messagebox.showinfo("OPTIMIZE","Recycle Bin emptied.")
   except Exception as e:messagebox.showerror("OPTIMIZE","Could not empty Recycle Bin. "+str(e))
  s.btn(s.body,"EMPTY RECYCLE BIN / إفراغ سلة المحذوفات",recycle).pack(anchor="w",pady=6)
  s.btn(s.body,"OPEN DISK CLEANUP / فتح تنظيف القرص",lambda:subprocess.Popen(["cleanmgr.exe"])).pack(anchor="w",pady=6)
  s.btn(s.body,"BACK / رجوع",s.optimize_now).pack(anchor="w",pady=12)
 def startup_tools(s):
  s.clear();s.head("apps","Review startup entries before disabling anything." if s.l=="en" else "راجع برامج بدء التشغيل قبل تعطيل أي عنصر.")
  tk.Label(s.body,text="Use Task Manager > Startup. Disable only apps you recognize and do not disable security, touchpad, audio or driver components.",bg=BG,fg=M,wraplength=760,justify="left").pack(anchor="w",pady=10)
  s.btn(s.body,"OPEN STARTUP MANAGER / فتح إدارة بدء التشغيل",lambda:subprocess.Popen(["taskmgr.exe"])).pack(anchor="w",pady=8)
  s.btn(s.body,"OPEN STARTUP FOLDER / فتح مجلد بدء التشغيل",lambda:os.startfile(os.path.expandvars(r"%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"))).pack(anchor="w",pady=8)
  s.btn(s.body,"BACK / رجوع",s.optimize_now).pack(anchor="w",pady=12)
 def memory_tools(s):
  s.clear();s.head("ram","Windows manages memory automatically. This page helps identify apps using the most RAM." if s.l=="en" else "ويندوز يدير الذاكرة تلقائياً. هذه الصفحة تعرض التطبيقات الأكثر استهلاكاً للرام.")
  mem=psutil.virtual_memory()
  tk.Label(s.body,text=f"RAM USED: {mem.percent}%   |   AVAILABLE: {mem.available/1048576:.0f} MB   |   TOTAL: {mem.total/1048576:.0f} MB",bg=P,fg=FG,font=("Segoe UI",13,"bold"),padx=14,pady=14).pack(fill="x",pady=8)
  s.btn(s.body,"REFRESH MEMORY / تحديث الذاكرة",s.memory_tools).pack(anchor="w",pady=6)
  s.btn(s.body,"OPEN TASK MANAGER / فتح إدارة المهام",lambda:subprocess.Popen(["taskmgr.exe"])).pack(anchor="w",pady=6)
  s.btn(s.body,"APP BOOSTER / معزز التطبيقات",s.apps).pack(anchor="w",pady=6)
  s.btn(s.body,"BACK / رجوع",s.optimize_now).pack(anchor="w",pady=12)
 def network_tools(s):
  s.clear();s.head("settings","Network commands may interrupt your connection." if s.l=="en" else "أوامر الشبكة قد تقطع الاتصال مؤقتاً.")
  def flush():
   if not messagebox.askyesno("OPTIMIZE","Flush the DNS resolver cache?"):return
   try:
    p=subprocess.run(["ipconfig.exe","/flushdns"],capture_output=True,text=True,timeout=30)
    messagebox.showinfo("OPTIMIZE",p.stdout or p.stderr or "Command completed.")
   except Exception as e:messagebox.showerror("OPTIMIZE",str(e))
  def reset():
   if not messagebox.askyesno("OPTIMIZE","Reset Winsock and TCP/IP settings? This may require Administrator rights and a restart."):return
   try:
    p=subprocess.run(["netsh.exe","winsock","reset"],capture_output=True,text=True,timeout=60)
    q=subprocess.run(["netsh.exe","int","ip","reset"],capture_output=True,text=True,timeout=60)
    messagebox.showinfo("OPTIMIZE",(p.stdout or p.stderr)+"\\n"+(q.stdout or q.stderr)+"\\nRestart Windows if requested.")
   except Exception as e:messagebox.showerror("OPTIMIZE",str(e))
  s.btn(s.body,"FLUSH DNS CACHE / مسح ذاكرة DNS",flush).pack(anchor="w",pady=6)
  s.btn(s.body,"OPEN NETWORK CONNECTIONS / إعدادات الشبكة",lambda:subprocess.Popen(["ncpa.cpl"])).pack(anchor="w",pady=6)
  s.btn(s.body,"RESET NETWORK STACK / إعادة ضبط الشبكة",reset).pack(anchor="w",pady=6)
  s.btn(s.body,"BACK / رجوع",s.optimize_now).pack(anchor="w",pady=12)
 def performance_tools(s):
  s.clear();s.head("dash","Choose one performance setting at a time." if s.l=="en" else "اختر إعداد أداء واحداً في كل مرة.")
  def power(guid,label):
   if not messagebox.askyesno("OPTIMIZE","Switch Windows power plan to "+label+"?"):return
   try:
    p=subprocess.run(["powercfg.exe","/setactive",guid],capture_output=True,text=True,timeout=30)
    if p.returncode:raise RuntimeError(p.stderr or p.stdout)
    messagebox.showinfo("OPTIMIZE","Power plan changed to "+label+".")
   except Exception as e:messagebox.showerror("OPTIMIZE",str(e))
  def drive():
   if not messagebox.askyesno("OPTIMIZE","Run Windows Optimize Drives on the system drive? Windows chooses the appropriate operation for SSD or HDD."):return
   try:subprocess.Popen(["defrag.exe",os.environ.get("SystemDrive","C:")+"\\","/O","/U","/V"])
   except Exception as e:messagebox.showerror("OPTIMIZE",str(e))
  s.btn(s.body,"BALANCED POWER PLAN / متوازن",lambda:power("381b4222-f694-41f0-9685-ff5bb260df2e","Balanced")).pack(anchor="w",pady=6)
  s.btn(s.body,"HIGH PERFORMANCE / أداء عالٍ",lambda:power("8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c","High performance")).pack(anchor="w",pady=6)
  s.btn(s.body,"OPTIMIZE DRIVES / تحسين الأقراص",drive).pack(anchor="w",pady=6)
  s.btn(s.body,"OPEN GAME MODE / فتح وضع الألعاب",lambda:os.startfile("ms-settings:gaming-gamemode")).pack(anchor="w",pady=6)
  s.btn(s.body,"BACK / رجوع",s.optimize_now).pack(anchor="w",pady=12)
 def repair_tools(s):
  s.clear();s.head("settings","System scans can take time. Run them individually as Administrator." if s.l=="en" else "فحوصات النظام قد تستغرق وقتاً. شغّل كل فحص منفرداً كمسؤول.")
  def run_scan(args,label):
   if not messagebox.askyesno("OPTIMIZE","Run "+label+"? This may take several minutes."):return
   try:
    subprocess.Popen(["cmd.exe","/k"]+args)
   except Exception as e:messagebox.showerror("OPTIMIZE",str(e))
  s.btn(s.body,"SFC /SCANNOW — CHECK SYSTEM FILES",lambda:run_scan(["sfc","/scannow"],"SFC scan")).pack(anchor="w",pady=6)
  s.btn(s.body,"DISM CHECKHEALTH",lambda:run_scan(["DISM","/Online","/Cleanup-Image","/CheckHealth"],"DISM CheckHealth")).pack(anchor="w",pady=6)
  s.btn(s.body,"DISM SCANHEALTH",lambda:run_scan(["DISM","/Online","/Cleanup-Image","/ScanHealth"],"DISM ScanHealth")).pack(anchor="w",pady=6)
  s.btn(s.body,"DISM RESTOREHEALTH",lambda:run_scan(["DISM","/Online","/Cleanup-Image","/RestoreHealth"],"DISM RestoreHealth")).pack(anchor="w",pady=6)
  s.btn(s.body,"BACK / رجوع",s.optimize_now).pack(anchor="w",pady=12)
 def uninstall_apps(s):
  if not messagebox.askyesno("OPTIMIZE", "Open Windows Apps and Features to uninstall programs?"):
   return
  try:os.startfile("appwiz.cpl")
  except Exception as e:messagebox.showerror("OPTIMIZE",str(e))
 def boost(s):
  try:
   if not s.pid:raise ValueError(s.t["noapp"])
   if not messagebox.askyesno("OPTIMIZE", "Set the selected process priority to Above Normal?\nThis may increase CPU usage for that app."):
    return
   psutil.Process(s.pid).nice(psutil.ABOVE_NORMAL_PRIORITY_CLASS);messagebox.showinfo("OPTIMIZE",s.t["boostok"])
  except Exception as e:messagebox.showerror("OPTIMIZE",s.t["boostfail"]+"\n"+str(e))
 def cleaner(s):
  s.clear();s.head("clean",s.t["warning"]);s.btn(s.body,s.t["cleanbtn"],s.clean).pack(anchor="w",pady=10)
 def clean(s,confirmed=False,show_restart=False):
  if not confirmed and not messagebox.askyesno("OPTIMIZE",s.t["ask"]):return
  d=x=0
  for root,ds,fs in os.walk(tempfile.gettempdir(),topdown=False):
   for n in fs:
    try:os.remove(os.path.join(root,n));d+=1
    except Exception:x+=1
   for n in ds:
    try:shutil.rmtree(os.path.join(root,n))
    except Exception:x+=1
  msg=s.t["done"].format(d,x);s.status.set(msg);messagebox.showinfo("OPTIMIZE",msg)
  if show_restart:
   messagebox.showinfo("OPTIMIZE","Optimization completed. Restart Windows for the best result." if s.l=="en" else "اكتمل التحسين. يُنصح بإعادة تشغيل ويندوز للحصول على أفضل نتيجة.")
 def restore(s):
  if not messagebox.askyesno("OPTIMIZE",s.t["askrp"]):return
  def job():
   try:ok=subprocess.run(["powershell.exe","-NoProfile","-Command","Checkpoint-Computer -Description 'OptimizeWin10 Before Changes' -RestorePointType MODIFY_SETTINGS"],capture_output=True,timeout=180).returncode==0
   except Exception:ok=False
   s.r.after(0,lambda:messagebox.showinfo("OPTIMIZE",s.t["rpok"]) if ok else messagebox.showwarning("OPTIMIZE",s.t["rpfail"]))
  threading.Thread(target=job,daemon=True).start()
 def scan(s):messagebox.showinfo("OPTIMIZE",f'CPU {psutil.cpu_percent()}% / RAM {psutil.virtual_memory().percent}%')
 def drivers(s):
  from tkinter import filedialog
  s.clear();s.head("drivers",s.t["drvsub"])
  s.driver_dir=os.path.join(os.path.dirname(sys.executable if getattr(sys,"frozen",False) else os.path.abspath(__file__)),"Drivers")
  s.driver_label=tk.Label(s.body,text=s.t["drvfolder"].format(s.driver_dir),bg=BG,fg=M,wraplength=850);s.driver_label.pack(anchor="w",pady=8)
  s.driver_list=tk.Listbox(s.body,bg=P,fg=FG,selectbackground="#444444",relief="flat",height=12);s.driver_list.pack(fill="both",expand=True,pady=8)
  def load():
   s.driver_list.delete(0,"end");s.driver_files=[]
   if os.path.isdir(s.driver_dir):
    for root,dirs,files in os.walk(s.driver_dir):
     for name in files:
      if name.lower().endswith(".inf"):s.driver_files.append(os.path.join(root,name))
   for path in s.driver_files:s.driver_list.insert("end",os.path.relpath(path,s.driver_dir))
   if not s.driver_files:messagebox.showinfo("OPTIMIZE",s.t["drvempty"])
  def choose():
   folder=filedialog.askdirectory(title=s.t["drvchoose"])
   if folder:s.driver_dir=folder;s.driver_label.config(text=s.t["drvfolder"].format(folder));load()
  def install():
   sel=s.driver_list.curselection()
   if not sel:messagebox.showwarning("OPTIMIZE",s.t["drvselect"]);return
   install_paths=[s.driver_files[i] for i in sel]
   run_install(install_paths)
  def install_all():
   load()
   if not s.driver_files:
    messagebox.showwarning("OPTIMIZE",s.t["drvempty"]);return
   run_install(s.driver_files)
  def run_install(paths):
   if not messagebox.askyesno("OPTIMIZE",s.t["drvconfirm"]+"\\n"+str(len(paths))+" INF package(s) will be checked by Windows."):
    return
   ok=0;failed=[]
   for path in paths:
    try:
     result=subprocess.run(["pnputil.exe","/add-driver",path,"/install"],capture_output=True,text=True,timeout=180)
     if result.returncode==0:ok+=1
     else:failed.append(os.path.basename(path)+": "+(result.stderr or result.stdout)[-350:])
    except Exception as e:failed.append(os.path.basename(path)+": "+str(e))
   report=("Windows processed "+str(ok)+" package(s).\\n")
   if failed:report+="Failed: "+str(len(failed))+"\\n"+"\\n".join(failed[:8])
   report+="\\nA successful command does not guarantee that a device needed this driver; check Device Manager."
   messagebox.showinfo("OPTIMIZE",report)
   s.status.set("Driver packages processed: "+str(ok)+" / "+str(len(paths)))
  def backup():
   folder=filedialog.askdirectory(title="Choose backup destination")
   if not folder:return
   try:
    result=subprocess.run(["pnputil.exe","/export-driver","* ",folder],capture_output=True,text=True,timeout=300)
    if result.returncode!=0:
     result=subprocess.run(["pnputil.exe","/export-driver","*",folder],capture_output=True,text=True,timeout=300)
    if result.returncode==0:messagebox.showinfo("OPTIMIZE","Driver backup completed.\\n"+result.stdout[-1000:])
    else:messagebox.showerror("OPTIMIZE",result.stderr[-1000:]+result.stdout[-1000:])
   except Exception as e:messagebox.showerror("OPTIMIZE",str(e))
  row=tk.Frame(s.body,bg=BG);row.pack(fill="x",pady=8)
  s.btn(row,s.t["drvchoose"],choose).pack(side="left",padx=(0,8))
  s.btn(row,s.t["drvinstall"],install).pack(side="left",padx=(0,8))
  s.btn(row,s.t["drvauto"],install_all).pack(side="left",padx=(0,8))
  s.btn(row,s.t["drvbackup"],backup).pack(side="left")
  load()
 def music(s):
  from tkinter import filedialog
  s.clear();s.head("music","10 Dan  •  Daklee / Joker Jr / Shiboba" if s.l=="en" else "10 Dan  •  داكلي / جوكر جونيور / شيبوبة")
  panel=tk.Frame(s.body,bg=P,padx=22,pady=20);panel.pack(fill="x",pady=10)
  tk.Label(panel,text="♫",bg=P,fg="#DDDDDD",font=("Segoe UI",42,"bold")).pack(pady=(0,4))
  tk.Label(panel,text="10 DAN",bg=P,fg=FG,font=("Segoe UI",20,"bold")).pack()
  tk.Label(panel,text="DAKLEE  •  JOKER JR  •  SHIBOBA",bg=P,fg=M,font=("Segoe UI",9,"bold")).pack(pady=(3,18))
  s.music_file=None;s.music_duration=375;s.music_paused=True
  s.music_status=tk.StringVar(value="Choose an audio file to start" if s.l=="en" else "اختر ملفًا صوتيًا للبدء")
  tk.Label(panel,textvariable=s.music_status,bg=P,fg=M).pack(pady=(0,10))
  def load():
   path=filedialog.askopenfilename(title="Choose audio" if s.l=="en" else "اختر ملفًا صوتيًا",filetypes=[("Audio files","*.mp3 *.wav *.ogg"),("All files","*.*")])
   if not path:return
   try:
    import pygame
    if not pygame.mixer.get_init():pygame.mixer.init()
    pygame.mixer.music.load(path);s.music_file=path
    from mutagen import File as AudioFile
    audio=AudioFile(path)
    if audio is None or not getattr(audio,"info",None):raise ValueError("Unsupported audio format")
    s.music_duration=max(1,int(audio.info.length))
    s.music_seek.config(to=s.music_duration);s.music_seek.set(0);s.music_paused=True
    s.music_status.set(os.path.basename(path));s.status.set("Audio loaded")
   except Exception as e:
    messagebox.showerror("OPTIMIZE","Could not load audio. Use MP3, WAV or OGG.\n"+str(e))
  def play():
   if not s.music_file:load()
   if not s.music_file:return
   try:
    import pygame
    if s.music_paused:
     if pygame.mixer.music.get_busy():pygame.mixer.music.unpause()
     else:pygame.mixer.music.play(start=max(0,s.music_seek.get()))
     s.music_paused=False
    else:pygame.mixer.music.pause();s.music_paused=True
    play_btn.config(text=("PLAY" if s.music_paused else "PAUSE"))
   except Exception as e:messagebox.showerror("OPTIMIZE",str(e))
  def stop():
   try:
    import pygame
    pygame.mixer.music.stop()
   except Exception:pass
   s.music_paused=True;s.music_seek.set(0);play_btn.config(text="PLAY")
  def seek(v):
   if not s.music_file:return
   try:
    import pygame
    playing=pygame.mixer.music.get_busy() and not s.music_paused
    pygame.mixer.music.play(start=max(0,float(v)))
    if not playing:pygame.mixer.music.pause()
    s.music_paused=not playing
    play_btn.config(text=("PAUSE" if playing else "PLAY"))
   except Exception:pass
  def jump(delta):
   if s.music_file:
    target=max(0,min(s.music_duration,s.music_seek.get()+delta));s.music_seek.set(target);seek(target)
  controls=tk.Frame(panel,bg=P);controls.pack(fill="x",pady=5)
  s.music_seek=tk.Scale(controls,from_=0,to=375,orient="horizontal",showvalue=False,bg=P,fg=FG,troughcolor="#444444",highlightthickness=0,activebackground="#DDDDDD",command=seek)
  s.music_seek.pack(fill="x")
  times=tk.Frame(controls,bg=P);times.pack(fill="x")
  s.music_time=tk.Label(times,text="00:00",bg=P,fg=M);s.music_time.pack(side="left")
  s.music_total=tk.Label(times,text="06:15",bg=P,fg=M);s.music_total.pack(side="right")
  buttons=tk.Frame(panel,bg=P);buttons.pack(pady=12)
  s.btn(buttons,"−10 SEC",lambda:jump(-10)).pack(side="left",padx=5)
  play_btn=s.btn(buttons,"PLAY",play);play_btn.pack(side="left",padx=5)
  s.btn(buttons,"STOP",stop).pack(side="left",padx=5)
  s.btn(buttons,"+10 SEC",lambda:jump(10)).pack(side="left",padx=5)
  s.btn(panel,"CHOOSE AUDIO FILE" if s.l=="en" else "اختيار ملف صوتي",load).pack(pady=(8,0))
  volrow=tk.Frame(s.body,bg=BG);volrow.pack(fill="x",pady=8)
  tk.Label(volrow,text="VOLUME / مستوى الصوت",bg=BG,fg=M).pack(anchor="w")
  def volume(v):
   try:
    import pygame
    if pygame.mixer.get_init():pygame.mixer.music.set_volume(float(v)/100)
   except Exception:pass
  tk.Scale(volrow,from_=0,to=100,orient="horizontal",showvalue=True,bg=BG,fg=FG,troughcolor="#444444",highlightthickness=0,command=volume).pack(fill="x")
  def update_time():
   if not s.body.winfo_exists():return
   try:
    import pygame
    if s.music_file and pygame.mixer.music.get_busy() and not s.music_paused:
     pos=max(0,pygame.mixer.music.get_pos()/1000)
     s.music_seek.set(min(s.music_duration,pos))
     s.music_time.config(text=f"{int(pos)//60:02d}:{int(pos)%60:02d}")
    s.music_total.config(text=f"{s.music_duration//60:02d}:{s.music_duration%60:02d}")
   except Exception:pass
   s.r.after(400,update_time)
  s.r.after(400,update_time)
 def toggle_windows_theme(s):
  import winreg,ctypes
  try:
   keypath=r"Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize"
   with winreg.CreateKey(winreg.HKEY_CURRENT_USER,keypath) as k:
    current=1
    try:current=winreg.QueryValueEx(k,"AppsUseLightTheme")[0]
    except OSError:pass
    value=0 if current else 1
    winreg.SetValueEx(k,"AppsUseLightTheme",0,winreg.REG_DWORD,value)
    winreg.SetValueEx(k,"SystemUsesLightTheme",0,winreg.REG_DWORD,value)
   try:
    HWND_BROADCAST=0xffff;WM_SETTINGCHANGE=0x001A;SMTO_ABORTIFHUNG=0x0002
    ctypes.windll.user32.SendMessageTimeoutW(HWND_BROADCAST,WM_SETTINGCHANGE,0,"ImmersiveColorSet",SMTO_ABORTIFHUNG,3000,None)
   except Exception:pass
   mode="Dark" if value==0 else "Light"
   s.status.set("Windows theme: "+mode)
   messagebox.showinfo("OPTIMIZE","Windows appearance switched to "+mode+" mode. Some apps may need to be reopened.")
  except Exception as e:messagebox.showerror("OPTIMIZE","Could not change Windows theme. "+str(e))
 def settings(s):
  s.clear();s.head("settings",s.t["manual"])
  s.btn(s.body,s.t["restore"],s.restore).pack(anchor="w",pady=8)
  s.btn(s.body,"TOGGLE WINDOWS DARK / LIGHT MODE — تبديل الوضع الداكن والفاتح",s.toggle_windows_theme).pack(anchor="w",pady=8)
  s.startup_btn=s.btn(s.body,"",s.toggle_startup);s.startup_btn.pack(anchor="w",pady=8)
  s.update_startup_label()
 def update_startup_label(s):
  try:
   import winreg
   with winreg.OpenKey(winreg.HKEY_CURRENT_USER,r"Software\Microsoft\Windows\CurrentVersion\Run") as k:winreg.QueryValueEx(k,"OptimizeWin10")
   enabled=True
  except Exception:enabled=False
  s.startup_enabled=enabled
  if hasattr(s,"startup_btn") and s.startup_btn.winfo_exists():
   s.startup_btn.config(text=("DISABLE APP STARTUP" if enabled else "ENABLE APP STARTUP") if s.l=="en" else ("إيقاف تشغيل التطبيق مع بدء ويندوز" if enabled else "تشغيل التطبيق مع بدء ويندوز"))
 def toggle_startup(s):
  try:
   import winreg
   with winreg.OpenKey(winreg.HKEY_CURRENT_USER,r"Software\Microsoft\Windows\CurrentVersion\Run",0,winreg.KEY_SET_VALUE) as k:
    if getattr(s,"startup_enabled",False):
     try:winreg.DeleteValue(k,"OptimizeWin10")
     except FileNotFoundError:pass
     s.status.set("App startup disabled")
    else:
     if getattr(sys,"frozen",False):cmd='"'+sys.executable+'"'
     else:cmd='"'+sys.executable+'" "'+os.path.abspath(__file__)+'"'
     winreg.SetValueEx(k,"OptimizeWin10",0,winreg.REG_SZ,cmd)
     s.status.set("App startup enabled")
   s.update_startup_label()
  except Exception as e:messagebox.showerror("OPTIMIZE",str(e))
 def toggle(s):
  s.l="ar" if s.l=="en" else "en";s.t=TXT[s.l];s.lb.config(text=s.t["lang"]);s.md.config(text=s.t["manual"])
  for k,b in s.nb:b.config(text=s.t[k])
  s.dashboard()
def launch():
 if os.name!="nt":raise SystemExit("Windows only")
 root=tk.Tk();root.title("OPTIMIZE WIN 10 v1.0");set_window_icon(root);root.geometry("820x540");root.configure(bg="#050505");root.resizable(False,False)
 shell=tk.Frame(root,bg="#0b0b0b",highlightbackground="#3A3A3A",highlightthickness=1);shell.place(relx=.5,rely=.5,anchor="center",width=710,height=440)
 logo=tk.Canvas(shell,width=112,height=96,bg="#0b0b0b",highlightthickness=0);logo.pack(pady=(38,10))
 logo.create_polygon(8,10,46,5,46,39,8,42,fill="#FFFFFF",outline="")
 logo.create_polygon(54,4,92,0,92,37,54,39,fill="#FFFFFF",outline="")
 logo.create_polygon(8,50,46,47,46,82,8,77,fill="#FFFFFF",outline="")
 logo.create_polygon(54,47,92,43,92,82,54,82,fill="#FFFFFF",outline="")
 tk.Label(shell,text="OPTIMIZE WIN 10  •  v1.0",bg="#0b0b0b",fg="#FFFFFF",font=("Segoe UI",25,"bold")).pack(pady=(2,2))
 tk.Label(shell,text="SYSTEM PERFORMANCE CENTER",bg="#0c0c0c",fg="#858585",font=("Segoe UI",9,"bold")).pack()
 msg=tk.Label(shell,text="INITIALIZING SYSTEM TOOLS...",bg="#0c0c0c",fg="#B8B8B8",font=("Segoe UI",9));msg.pack(pady=(22,8))
 style=ttk.Style(root);style.theme_use("clam");style.configure("Load.Horizontal.TProgressbar",troughcolor="#242424",background="#F2F2F2",bordercolor="#242424",lightcolor="#F2F2F2",darkcolor="#F2F2F2")
 bar=ttk.Progressbar(shell,mode="indeterminate",length=420,style="Load.Horizontal.TProgressbar");bar.pack(pady=5);bar.start(10)
 def choose():
  bar.stop();msg.config(text="SELECT YOUR LANGUAGE  /  اختر اللغة")
  row=tk.Frame(shell,bg="#0c0c0c");row.pack(pady=22)
  def go(lang):
   root.destroy();win=tk.Tk();set_window_icon(win);App(win,lang);win.mainloop()
  for label,lang in [("العربية","ar"),("ENGLISH","en")]:
   tk.Button(row,text=label,command=lambda x=lang:go(x),bg="#202020",fg="#FFFFFF",activebackground="#353535",activeforeground="#FFFFFF",relief="flat",bd=0,padx=30,pady=13,font=("Segoe UI",10,"bold"),cursor="hand2").pack(side="left",padx=8)
 tk.Label(shell,text="MANUAL CONTROL  •  SAFE SYSTEM TWEAKS",bg="#0c0c0c",fg="#666666",font=("Segoe UI",8)).pack(side="bottom",pady=16)
 root.after(1500,choose);root.mainloop()
if __name__=="__main__":launch()
