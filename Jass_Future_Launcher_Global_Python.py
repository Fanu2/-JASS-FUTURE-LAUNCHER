import sys, os, json, shutil, subprocess
from pathlib import Path
from datetime import datetime
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication,QMainWindow,QWidget,QLabel,QPushButton,QLineEdit,QComboBox,QScrollArea,QGridLayout,QVBoxLayout,QHBoxLayout,QFrame,QFileDialog,QMessageBox,QMenu

APP_NAME='JASS FUTURE LAUNCHER'
CONFIG_DIR=Path(os.environ.get('APPDATA',Path.home()))/'JassFutureLauncher'
CONFIG_FILE=CONFIG_DIR/'apps.json'
EXCLUDED={'.git','.venv','venv','env','__pycache__','node_modules','.pytest_cache','.mypy_cache','.idea','.vscode','site-packages'}
SUPPORTED={'.py','.pyw','.exe','.bat','.cmd','.lnk'}
HINTS={'AI':['ai','athena','llm','rag','assistant','ollama'],'MEDIA':['video','audio','subtitle','srt','movie','music','image','photo'],'LANGUAGE':['language','grammar','mizo','punjabi','spanish','french','english','translit'],'TOOLS':['tool','utility','launcher','studio','maker','lab'],'DEVELOPMENT':['dev','code','python','project','git'],'DOCUMENTS':['pdf','doc','book','epub','ocr','document'],'REVENUE':['revenue','hrtk','jamabandi','khewat','khasra']}
ICONS={'AI':'🤖','MEDIA':'🎬','LANGUAGE':'🌐','TOOLS':'🧰','DEVELOPMENT':'💻','DOCUMENTS':'📚','REVENUE':'🏛️','OTHER':'🚀'}
STYLE='''QMainWindow,QWidget{background:#090d18;color:#edf2ff;font-family:"Segoe UI";} QLabel#title{font-size:30px;font-weight:800;color:#fff;} QLabel#subtitle{color:#8f9bb7;font-size:13px;} QFrame#topbar{background:#101728;border:1px solid #263451;border-radius:18px;} QFrame#card{background:#111a2b;border:1px solid #293a5d;border-radius:18px;} QFrame#card:hover{border:1px solid #8b5cf6;background:#151f34;} QLabel#appIcon{font-size:42px;} QLabel#appName{font-size:17px;font-weight:750;color:#fff;} QLabel#meta{color:#8f9bb7;font-size:11px;} QPushButton{background:#7c4dff;border:0;border-radius:10px;padding:9px 14px;color:white;font-weight:700;} QPushButton:hover{background:#986fff;} QPushButton#secondary{background:#202c45;} QPushButton#secondary:hover{background:#2c3b5b;} QPushButton#favorite{background:transparent;font-size:20px;padding:2px;} QLineEdit,QComboBox{background:#0b1120;border:1px solid #2b3a58;border-radius:10px;padding:9px 12px;color:#edf2ff;} QScrollArea{border:0;background:transparent;} QMenu{background:#121a2a;border:1px solid #344665;color:#fff;} QMenu::item:selected{background:#263756;}'''

def pretty(p):
    s=p.stem.replace('_',' ').replace('-',' ').strip()
    return ' '.join(w.capitalize() if w.islower() else w for w in s.split())
def category(p):
    s=p.stem.lower()
    for c,h in HINTS.items():
        if any(x in s for x in h): return c
    return 'OTHER'

class Card(QFrame):
    def __init__(self,r,owner):
        super().__init__(); self.r=r; self.owner=owner; self.setObjectName('card'); self.setMinimumSize(275,210)
        icon=QLabel(ICONS.get(r['category'],'🚀')); icon.setObjectName('appIcon'); icon.setAlignment(Qt.AlignCenter)
        name=QLabel(r['name']); name.setObjectName('appName'); name.setWordWrap(True); name.setAlignment(Qt.AlignCenter)
        meta=QLabel(f"{r['category']} • {r['type'].upper()}"); meta.setObjectName('meta'); meta.setAlignment(Qt.AlignCenter)
        loc=QLabel(r['path']); loc.setObjectName('meta'); loc.setWordWrap(True); loc.setAlignment(Qt.AlignCenter)
        row=QHBoxLayout(); b=QPushButton('▶ Launch'); b.clicked.connect(lambda:self.owner.launch(r)); row.addWidget(b)
        f=QPushButton('★' if r.get('favorite') else '☆'); f.setObjectName('favorite'); f.clicked.connect(lambda:self.owner.favorite(r['path'])); row.addWidget(f)
        m=QPushButton('⋮'); m.setObjectName('secondary'); m.clicked.connect(self.menu); row.addWidget(m)
        l=QVBoxLayout(self); l.setContentsMargins(16,14,16,14); l.setSpacing(7); l.addWidget(icon); l.addWidget(name); l.addWidget(meta); l.addWidget(loc,1); l.addLayout(row)
    def menu(self):
        m=QMenu(self); a=m.addAction('📁 Open containing folder'); b=m.addAction('✕ Remove from launcher'); x=m.exec(self.mapToGlobal(self.rect().bottomLeft()))
        if x==a:self.owner.open_folder(self.r['path'])
        elif x==b:self.owner.remove(self.r['path'])

class Launcher(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle(APP_NAME); self.resize(1280,850); self.setMinimumSize(1000,700); self.setStyleSheet(STYLE); self.records=[]; self.downloads=Path.home()/'Downloads'; self.build(); self.load(); self.scan(); self.refresh()
    def build(self):
        root=QWidget(); self.setCentralWidget(root); out=QVBoxLayout(root); out.setContentsMargins(22,20,22,20); out.setSpacing(14)
        top=QFrame(); top.setObjectName('topbar'); h=QHBoxLayout(top); h.setContentsMargins(22,16,22,16); v=QVBoxLayout(); t=QLabel('🚀 JASS FUTURE LAUNCHER'); t.setObjectName('title'); s=QLabel('Your PySide6 applications • one click away'); s.setObjectName('subtitle'); v.addWidget(t); v.addWidget(s); h.addLayout(v); h.addStretch(); self.status=QLabel(); self.status.setObjectName('subtitle'); h.addWidget(self.status); out.addWidget(top)
        bar=QHBoxLayout(); self.search=QLineEdit(); self.search.setPlaceholderText('🔎 Search applications…'); self.search.textChanged.connect(self.refresh); bar.addWidget(self.search,1)
        self.cat=QComboBox(); self.cat.addItem('All categories'); self.cat.currentTextChanged.connect(self.refresh); bar.addWidget(self.cat)
        fav=QPushButton('★ Favorites'); fav.setObjectName('secondary'); fav.clicked.connect(self.show_favorites); bar.addWidget(fav)
        add=QPushButton('＋ Add App'); add.clicked.connect(self.add); bar.addWidget(add)
        scan=QPushButton('↻ Scan'); scan.setObjectName('secondary'); scan.clicked.connect(self.rescan); bar.addWidget(scan)
        folder=QPushButton('📁 Downloads'); folder.setObjectName('secondary'); folder.clicked.connect(lambda:self.open_folder(str(self.downloads))); bar.addWidget(folder); out.addLayout(bar)
        self.stats=QLabel(); self.stats.setObjectName('subtitle'); out.addWidget(self.stats)
        self.scroll=QScrollArea(); self.scroll.setWidgetResizable(True); self.container=QWidget(); self.grid=QGridLayout(self.container); self.grid.setContentsMargins(5,5,5,30); self.grid.setSpacing(14); self.scroll.setWidget(self.container); out.addWidget(self.scroll,1)
    def load(self):
        CONFIG_DIR.mkdir(parents=True,exist_ok=True)
        try:self.records=json.loads(CONFIG_FILE.read_text(encoding='utf-8')).get('apps',[]) if CONFIG_FILE.exists() else []
        except Exception:self.records=[]
    def save(self):
        CONFIG_DIR.mkdir(parents=True,exist_ok=True); CONFIG_FILE.write_text(json.dumps({'apps':self.records},indent=2,ensure_ascii=False),encoding='utf-8')
    def scan(self):
        found={}
        if self.downloads.exists():
            for p in self.downloads.rglob('*'):
                try:
                    if p.is_file() and p.suffix.lower() in SUPPORTED and not any(x.lower() in EXCLUDED for x in p.parts) and not p.name.startswith(('.', '~')): found[str(p.resolve())]=p
                except (OSError,PermissionError): pass
        old={r['path']:r for r in self.records}; merged={}
        for path,p in found.items():
            r=old.get(path,{})
            merged[path]={'path':path,'name':r.get('name') or pretty(p),'category':r.get('category') or category(p),'type':p.suffix.lower().lstrip('.'),'favorite':bool(r.get('favorite',False)),'last_launch':r.get('last_launch','')}
        for r in self.records:
            if r['path'] not in merged and r.get('manual'): merged[r['path']]=r
        self.records=sorted(merged.values(),key=lambda r:(not r.get('favorite',False),r['name'].lower())); self.save(); self.update_categories(); self.status.setText(f'{len(self.records)} apps • {self.downloads}')
    def update_categories(self):
        cur=self.cat.currentText(); cats=sorted({r['category'] for r in self.records}); self.cat.blockSignals(True); self.cat.clear(); self.cat.addItem('All categories'); self.cat.addItems(cats); self.cat.setCurrentText(cur if cur in cats or cur=='All categories' else 'All categories'); self.cat.blockSignals(False)
    def filtered(self):
        q=self.search.text().lower().strip(); c=self.cat.currentText(); return [r for r in self.records if (c=='All categories' or r['category']==c) and (not q or q in (r['name']+' '+r['path']+' '+r['category']).lower())]
    def refresh(self):
        while self.grid.count():
            x=self.grid.takeAt(0); w=x.widget()
            if w:w.deleteLater()
        rs=self.filtered()
        for i,r in enumerate(rs):self.grid.addWidget(Card(r,self),i//3,i%3)
        self.stats.setText(f'{len(rs)} shown • {len(self.records)} total • {sum(r.get("favorite",False) for r in self.records)} favorites')
    def show_favorites(self):
        self.search.clear(); self.cat.setCurrentText('All categories')
        while self.grid.count():
            x=self.grid.takeAt(0); w=x.widget()
            if w:w.deleteLater()
        rs=[r for r in self.records if r.get('favorite')]
        for i,r in enumerate(rs):self.grid.addWidget(Card(r,self),i//3,i%3)
        self.stats.setText(f'{len(rs)} favorite applications')
    def launch(self,r):
        p=Path(r['path'])
        if not p.exists(): QMessageBox.warning(self,'Application not found',f'No longer exists:\n\n{p}'); self.rescan(); return
        try:
            ext=p.suffix.lower()
            if ext in {'.lnk','.exe','.bat','.cmd'}: os.startfile(str(p))
            elif ext in {'.py','.pyw'}:
                py=shutil.which('py') or sys.executable; subprocess.Popen([py,str(p)],cwd=str(p.parent))
            r['last_launch']=datetime.now().isoformat(timespec='seconds'); self.save()
        except Exception as e: QMessageBox.critical(self,'Launch failed',f'Could not launch:\n\n{p}\n\n{e}')
    def favorite(self,path):
        for r in self.records:
            if r['path']==path:r['favorite']=not r.get('favorite',False); break
        self.save(); self.refresh()
    def remove(self,path):self.records=[r for r in self.records if r['path']!=path]; self.save(); self.refresh()
    def open_folder(self,path):
        try: os.startfile(str(Path(path) if Path(path).is_dir() else Path(path).parent))
        except Exception as e: QMessageBox.warning(self,'Cannot open folder',str(e))
    def add(self):
        files,_=QFileDialog.getOpenFileNames(self,'Add applications',str(self.downloads),'Applications (*.py *.pyw *.exe *.bat *.cmd *.lnk);;All files (*.*)')
        existing={r['path'] for r in self.records}
        for f in files:
            p=Path(f).resolve(); path=str(p)
            if path not in existing:self.records.append({'path':path,'name':pretty(p),'category':category(p),'type':p.suffix.lower().lstrip('.'),'favorite':False,'last_launch':'','manual':True})
        self.records.sort(key=lambda r:(not r.get('favorite',False),r['name'].lower())); self.save(); self.update_categories(); self.refresh()
    def rescan(self):self.scan(); self.refresh()

if __name__=='__main__':
    app=QApplication(sys.argv); app.setApplicationName(APP_NAME); app.setFont(QFont('Segoe UI',10)); w=Launcher(); w.show(); sys.exit(app.exec())
