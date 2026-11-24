import os,sys,shutil,tempfile,subprocess,threading,tkinter as tk
from tkinter import ttk,messagebox
import psutil
BG="#000000"; P="#111111"; FG="#eeeeee"; M="#999999"
TXT={"en":{"dash":"DASHBOARD","apps":"APP BOOSTER","clean":"DISK CLEANER","settings":"SETTINGS","cpu":"CPU","ram":"RAM","disk":"DISK","refresh":"REFRESH","choose":"Choose a running process","boost":"SET ABOVE NORMAL","cleanbtn":"CLEAN TEMP FILES","restore":"CREATE RESTORE POINT","startup":"ENABLE STARTUP SCAN","manual":"MANUAL MODE — changes need your action","warning":"Conservative tools. No Windows services disabled; Realtime priority is excluded.","lang":"العربية","ask":"Delete temporary files? Files in use are skipped.","done":"Deleted {} files; skipped {}.","askrp":"Request a Windows restore point? Admin rights/System Protection may be required.","rpok":"Restore point command completed.","rpfail":"Restore point failed. Run as Administrator and check System Protection.","noapp":"Select a process first.","boostok":"Priority set to Above Normal.","boostfail":"Could not change priority."},"ar":{"dash":"لوحة التحكم","apps":"معزز التطبيقات","clean":"تنظيف الملفات","settings":"الإعدادات","cpu":"المعالج","ram":"الذاكرة","disk":"القرص","refresh":"تحديث","choose":"اختر عملية قيد التشغيل","boost":"تعيين أولوية أعلى من العادية","cleanbtn":"تنظيف الملفات المؤقتة","restore":"إنشاء نقطة استعادة","startup":"تفعيل فحص بدء التشغيل","manual":"الوضع اليدوي — التغييرات بموافقتك","warning":"أدوات محافظة. لا نعطّل خدمات ويندوز ولا نستخدم أولوية الوقت الحقيقي.","lang":"English","ask":"حذف الملفات المؤقتة؟ سيتم تخطي الملفات المستخدمة.","done":"تم حذف {} ملف وتخطي {}.","askrp":"طلب إنشاء نقطة استعادة؟ قد تحتاج صلاحيات المسؤول وحماية النظام.","rpok":"اكتمل أمر نقطة الاستعادة.","rpfail":"فشل إنشاء نقطة الاستعادة. شغّل كمسؤول وتحقق من حماية النظام.","noapp":"اختر عملية أولاً.","boostok":"تم تعيين الأولوية أعلى من العادية.","boostfail":"تعذر تغيير الأولوية."}}
class App:
 def __init__(s,r,lang="en"):
  s.r=r;s.l=lang;s.t=TXT[s.l];s.pid=None;r.title("OPTIMIZE WIN 10");r.geometry("950x650");r.configure(bg=BG);r.minsize(800,520)
  h=tk.Frame(r,bg=BG);h.pack(fill="x",padx=20,pady=16);tk.Label(h,text="OPTIMIZE WIN 10",bg=BG,fg=FG,font=("Segoe UI",20,"bold")).pack(side="left")
  s.lb=s.btn(h,"العربية",s.toggle);s.lb.pack(side="right");s.md=tk.Label(h,text=s.t["manual"],bg=BG,fg=M);s.md.pack(side="right",padx=16)
  s.nav=tk.Frame(r,bg=BG);s.nav.pack(fill="x",padx=20);s.body=tk.Frame(r,bg=BG);s.body.pack(fill="both",expand=True,padx=20,pady=14)
  s.status=tk.StringVar(value="Ready");tk.Label(r,textvariable=s.status,bg="#080808",fg=M,anchor="w",padx=20,pady=8).pack(fill="x",side="bottom")
  s.nb=[]
  for k,f in [("dash",s.dashboard),("apps",s.apps),("clean",s.cleaner),("settings",s.settings)]:
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
  s.clear();s.head("dash",s.t["warning"]);row=tk.Frame(s.body,bg=BG);row.pack(fill="x",pady=8);s.v={}
  for k in ("cpu","ram","disk"):
   f=tk.Frame(row,bg=P,padx=18,pady=14);f.pack(side="left",fill="both",expand=True,padx=(0,10));tk.Label(f,text=s.t[k],bg=P,fg=M).pack(anchor="w");v=tk.Label(f,text="--",bg=P,fg=FG,font=("Segoe UI",23,"bold"));v.pack(anchor="w",pady=8);s.v[k]=v
  s.btn(s.body,s.t["refresh"],s.refresh).pack(anchor="e",pady=8);s.tree(10)
 def tick(s):
  try:
   if hasattr(s,"v"):
    s.v["cpu"].config(text=f"{psutil.cpu_percent()}%");s.v["ram"].config(text=f"{psutil.virtual_memory().percent}%");s.v["disk"].config(text=f"{psutil.disk_usage(os.environ.get('SystemDrive','C:')+'\\').percent}%")
  except Exception:pass
  s.r.after(2500,s.tick)
 def apps(s):
  s.clear();s.head("apps",s.t["warning"]);tk.Label(s.body,text=s.t["choose"],bg=BG,fg=FG).pack(anchor="w");s.tree(14);s.btn(s.body,s.t["boost"],s.boost).pack(anchor="w",pady=10)
 def boost(s):
  try:
   if not s.pid:raise ValueError(s.t["noapp"])
   psutil.Process(s.pid).nice(psutil.ABOVE_NORMAL_PRIORITY_CLASS);messagebox.showinfo("OPTIMIZE",s.t["boostok"])
  except Exception as e:messagebox.showerror("OPTIMIZE",s.t["boostfail"]+"\n"+str(e))
 def cleaner(s):
  s.clear();s.head("clean",s.t["warning"]);s.btn(s.body,s.t["cleanbtn"],s.clean).pack(anchor="w",pady=10)
 def clean(s):
  if not messagebox.askyesno("OPTIMIZE",s.t["ask"]):return
  d=x=0
  for root,ds,fs in os.walk(tempfile.gettempdir(),topdown=False):
   for n in fs:
    try:os.remove(os.path.join(root,n));d+=1
    except Exception:x+=1
   for n in ds:
    try:shutil.rmtree(os.path.join(root,n))
    except Exception:x+=1
  msg=s.t["done"].format(d,x);s.status.set(msg);messagebox.showinfo("OPTIMIZE",msg)
 def restore(s):
  if not messagebox.askyesno("OPTIMIZE",s.t["askrp"]):return
  def job():
   try:ok=subprocess.run(["powershell.exe","-NoProfile","-Command","Checkpoint-Computer -Description 'OptimizeWin10 Before Changes' -RestorePointType MODIFY_SETTINGS"],capture_output=True,timeout=180).returncode==0
   except Exception:ok=False
   s.r.after(0,lambda:messagebox.showinfo("OPTIMIZE",s.t["rpok"]) if ok else messagebox.showwarning("OPTIMIZE",s.t["rpfail"]))
  threading.Thread(target=job,daemon=True).start()
 def scan(s):messagebox.showinfo("OPTIMIZE",f'CPU {psutil.cpu_percent()}% / RAM {psutil.virtual_memory().percent}%')
 def settings(s):
  s.clear();s.head("settings",s.t["manual"]);s.btn(s.body,s.t["restore"],s.restore).pack(anchor="w",pady=8);s.btn(s.body,s.t["startup"],s.startup).pack(anchor="w",pady=8)
 def startup(s):
  try:
   import winreg
   cmd=f'"{sys.executable}" --startup-scan' if getattr(sys,"frozen",False) else f'"{sys.executable}" "{os.path.abspath(__file__)}" --startup-scan'
   with winreg.OpenKey(winreg.HKEY_CURRENT_USER,r"Software\Microsoft\Windows\CurrentVersion\Run",0,winreg.KEY_SET_VALUE) as k:winreg.SetValueEx(k,"OptimizeWin10",0,winreg.REG_SZ,cmd)
   s.status.set("Startup scan enabled")
  except Exception as e:messagebox.showerror("OPTIMIZE",str(e))
 def toggle(s):
  s.l="ar" if s.l=="en" else "en";s.t=TXT[s.l];s.lb.config(text=s.t["lang"]);s.md.config(text=s.t["manual"])
  for k,b in s.nb:b.config(text=s.t[k])
  s.dashboard()
def launch():
 if os.name!="nt":raise SystemExit("Windows only")
 root=tk.Tk();root.title("OPTIMIZE WIN 10");root.geometry("620x360");root.configure(bg="#000000");root.resizable(False,False)
 tk.Label(root,text="OPTIMIZE WIN 10",bg="#000000",fg="#eeeeee",font=("Segoe UI",24,"bold")).pack(pady=(55,12))
 msg=tk.Label(root,text="LOADING...",bg="#000000",fg="#888888",font=("Segoe UI",10));msg.pack()
 bar=ttk.Progressbar(root,mode="indeterminate",length=260);bar.pack(pady=22);bar.start(12)
 def choose():
  bar.stop();msg.config(text="CHOOSE LANGUAGE / اختر اللغة")
  row=tk.Frame(root,bg="#000000");row.pack(pady=20)
  def go(lang):
   root.destroy();win=tk.Tk();App(win,lang);win.mainloop()
  tk.Button(row,text="العربية",command=lambda:go("ar"),bg="#191919",fg="white",relief="flat",padx=25,pady=12).pack(side="left",padx=10)
  tk.Button(row,text="English",command=lambda:go("en"),bg="#191919",fg="white",relief="flat",padx=25,pady=12).pack(side="left",padx=10)
 root.after(1100,choose);root.mainloop()
if __name__=="__main__":launch()
