#!/usr/bin/env python3
"""Actualiza V19 a V20 sin tocar los perfiles cifrados ni credenciales."""
from pathlib import Path
import shutil,subprocess,time,sys
root=Path.home()/'citas-tie'
files=['rapido.mjs','ui-adb.mjs','vigilar.mjs','instalar.sh']
for f in files:
    if not (root/f).is_file(): raise SystemExit('Falta archivo local '+f)
changes={f:(root/f).read_text() for f in files}
def swap(f,a,b):
    s=changes[f]
    if s.count(a)!=1: raise ValueError(f+': versión o texto distinto')
    changes[f]=s.replace(a,b,1)
def section(f,start,end,new):
    s=changes[f]; i=s.index(start);j=s.index(end,i+len(start))
    changes[f]=s[:i]+new+s[j:]

if 'ultimo-acceso-v20' not in changes['rapido.mjs']:
    swap('rapido.mjs','openClaveOnCurrentPage,fillApplicantDetailsFromAuthenticatedPage','openSinClaveOnCurrentPage,fillApplicantDetailsFromAuthenticatedPage')
    swap('rapido.mjs',"const START='2026-10-17'", "const ACCESS_MODE=path.join(CONFIG,'ultimo-acceso-v20');\nconst START='2026-10-17'")
    swap('rapido.mjs',"if(/presentacion con cl@ve/.test(text)&&/presentacion sin cl@ve/.test(text))return 'clave';", "if(/presentacion (?:con|sin) cl@ve/.test(text) && /(cita previa extranjeria|sede electronica|lee atentamente)/.test(text))return 'clave';")
    section('rapido.mjs','function foregroundChrome(){','\nfunction openOfficial(){', '''function foregroundChrome(){
 const isChrome=()=>/mCurrentFocus=[^\\r\\n]*com\\.android\\.chrome/.test(adb(['shell','dumpsys','window'],13000));
 if(isChrome())return;
 console.log('Recuperando Chrome del segundo plano…');
 // REORDER_TO_FRONT reutiliza la actividad abierta, sin navegar a Google.
 adb(['shell','am','start','-a','android.intent.action.MAIN','-c','android.intent.category.LAUNCHER',
 '-n','com.android.chrome/com.google.android.apps.chrome.Main','-f','0x00020000'],13000);
 if(!isChrome())throw new Error('Chrome sigue fuera de primer plano');
}
''')
    swap('rapido.mjs','for(let i=0;i<4;i++){\n  const nodes=dump();','for(let i=0;i<7;i++){\n  const nodes=dump();')
    section('rapido.mjs',"  if(stage==='clave'){","  if(stage==='solicitante'){", """  if(stage==='clave'){
   const ok=await openSinClaveOnCurrentPage();
   if(!ok){console.log('No se reconoce la entrada sin Cl@ve.');return}
   fs.mkdirSync(CONFIG,{recursive:true,mode:0o700});
   fs.writeFileSync(ACCESS_MODE,'SIN_CLAVE',{mode:0o600});
   await delay(400);continue;
  }
""")
    swap('rapido.mjs','   const filled=await fillApplicantDetailsFromAuthenticatedPage(p);',"   const withoutClave=fs.existsSync(ACCESS_MODE) && fs.readFileSync(ACCESS_MODE,'utf8').trim()==='SIN_CLAVE';\n   const filled=await fillApplicantDetailsFromAuthenticatedPage(p,{withoutClave});")

if 'openSinClaveOnCurrentPage' not in changes['ui-adb.mjs']:
    section('ui-adb.mjs','async function prepare(){','\nasync function saveScreen(){', '''async function prepare(){
 checkAdb();
 // No reabrir la URL inicial; se conserva la sesión y el paso alcanzado.
 const w=cmd(['shell','dumpsys','window'],{ms:14000});
 if(!/mCurrentFocus=[^\\r\\n]*com\\.android\\.chrome/.test(w))
  throw new Error('Chrome no está visible');
 await sleep(250);
}
''')
    start='\n// V14 — DATOS DEL SOLICITANTE AUTENTICADO'
    entry='''
// Desplazarse hasta la tarjeta oficial Sin Cl@ve en la misma página.
export async function openSinClaveOnCurrentPage(){
 try{
  checkAdb();wakeCurrentChrome();let nodes=await dump(),seen=false;
  for(let i=0;i<9;i++){
   if(stopMessage(nodes))throw new Error(stopMessage(nodes));
   const text=fullPageText(nodes);
   if(/presentacion con cl@ve|presentacion sin cl@ve/.test(text))seen=true;
   if(!seen && i>0)throw new Error('No se reconoce la pantalla oficial');
   let hits=uniqueByBounds(nodes.filter(n=>n.enabled&&n.x>0&&n.y>0&&
    /^presentacion sin cl@ve(?:\\s|$)/.test(norm(n.text||n.desc))));
   if(hits.length>1){const clickable=hits.filter(n=>n.clickable);if(clickable.length===1)hits=clickable}
   if(hits.length===1){tap(hits[0]);await sleep(1250);
    const next=fullPageText(await dump());
    if(!/introduce los datos del solicitante|nombre y apellidos|tipo de documento/.test(next))
      throw new Error('No se ha verificado el formulario del solicitante');
    console.log('Formulario oficial sin Cl@ve abierto');return true;
   }
   if(hits.length>1)throw new Error('Opción Sin Cl@ve duplicada');
   scrollApplicantForm('down');await sleep(400);nodes=await dump();
  }
  throw new Error('Sin Cl@ve no aparece en la pantalla');
 }catch(e){console.log('ENTRADA DETENIDA:',e.message);return false}
}
'''
    swap('ui-adb.mjs',start,'\n'+entry+start)
    swap('ui-adb.mjs', 'export async function fillApplicantDetailsFromAuthenticatedPage(profile){', 'export async function fillApplicantDetailsFromAuthenticatedPage(profile,{withoutClave=false}={}){')
    section('ui-adb.mjs','  // Comprobación segura de identidad en la cabecera;','  await seekApplicantFields();', '''  if(!withoutClave){await seekAuthenticatedPresenter();}
  else{
   const screen=fullPageText(await dump());
   if(/usuario clave/.test(screen))throw new Error('Sesión autenticada inesperada; no mezclar presentadores');
  }
''')

if 'V20:' not in changes['vigilar.mjs']:
    swap('vigilar.mjs','CITAS TIE · MOVIL V19','CITAS TIE · MOVIL V20')
    swap('vigilar.mjs','V19: no crea nuevas pestañas de Google; comprueba con Chrome abierto y Android desbloqueado.','V20: reanuda Chrome y utiliza la entrada oficial sin Cl@ve.')
if 'MOVIL V20 INSTALADO' not in changes['instalar.sh']:
    swap('instalar.sh','MOVIL V19 INSTALADO','MOVIL V20 INSTALADO')

# Prevalidación completa antes de reemplazar un solo archivo.
backup=root/('.citas-v19-copia-'+str(int(time.time())))
backup.mkdir(mode=0o700)
changed=[f for f in files if changes[f]!=(root/f).read_text()]
try:
    for f in changed:
        shutil.copy2(root/f,backup/f)
        tmp=root/(f+'.tmp-v20')
        tmp.write_text(changes[f]);tmp.replace(root/f)
    for f in ['rapido.mjs','ui-adb.mjs','vigilar.mjs','final-ui.mjs']:
        subprocess.run(['node','--check',f],cwd=root,check=True,timeout=15)
except Exception:
    for f in changed:
        if (backup/f).exists():shutil.copy2(backup/f,root/f)
    raise SystemExit('Error: cambios revertidos. Archivos anteriores conservados.')
print('V20 CORREGIDA Y VALIDADA. Perfil cifrado intacto.')
