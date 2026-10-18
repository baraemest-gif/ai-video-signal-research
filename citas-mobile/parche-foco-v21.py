#!/usr/bin/env python3
"""Corrección V21: reconocimiento del portal visible por Android UIAutomator.
No toca perfil, claves, certificados, tareas de Windows ni citas.
"""
from pathlib import Path
import subprocess, shutil, time
base=Path.cwd()
reg=r'provincias disponibles|selecciona provincia|provincia seleccionada|tramites policia nacional|presentacion (?:con|sin) cl@ve|introduce los datos del solicitante|tipo de documento|pais de nacionalidad|solicitar cita|datos de la cita|no hay citas disponibles'
files={n:(base/n).read_text() for n in ('rapido.mjs','ui-adb.mjs')}
a,b=files['rapido.mjs'],files['ui-adb.mjs']
if 'La sede oficial no aparece delante' in a and 'async function wakeCurrentChrome(){' in b:
 print('CORRECCIÓN YA INSTALADA. No se realizan más cambios.')
 raise SystemExit(0)
begin='function foregroundChrome(){'
end='\nfunction openOfficial(){'
assert a.count(begin)==1 and a.count(end)==1, 'Rapido V21 no reconocida'
one='''function foregroundChrome(){
 const official=()=>{
  const ns=dump();
  const page=normal(ns.map(n=>n.text+' '+n.desc).join(' '));
  return /%s/.test(page);
 };
 if(official())return;
 console.log('Recuperando Chrome sin reiniciar la cita…');
 adb(['shell','am','start','-n','com.android.chrome/com.google.android.apps.chrome.Main','-f','0x00020000'],13000);
 if(!official())throw new Error('La sede oficial no aparece delante; no se pulsa otra aplicación.');
}
'''%reg
a=a[:a.index(begin)]+one+a[a.index(end):]
start='async function prepare(){'; finish='\nasync function saveScreen(){'
assert b.count(start)==1 and b.count(finish)==1, 'UI V21 no reconocida'
one='''async function prepare(){
 checkAdb();
 await wakeCurrentChrome();
 await sleep(250);
}
'''
b=b[:b.index(start)]+one+b[b.index(finish):]
start='function wakeCurrentChrome(){';finish='\nfunction exactPoliceHuellas(t){'
assert b.count(start)==1 and b.count(finish)==1, 'Validación de Chrome inesperada'
one='''async function wakeCurrentChrome(){
 const page=norm((await dump()).map(n=>n.text+' '+n.desc).join(' '));
 if(!/%s/.test(page))
  throw new Error('No se ve la sede oficial en pantalla; no se pulsará otra aplicación.');
}
'''%reg
b=b[:b.index(start)]+one+b[b.index(finish):]
assert b.count('wakeCurrentChrome();')>=3
b=b.replace('wakeCurrentChrome();','await wakeCurrentChrome();')
b=b.replace('await await wakeCurrentChrome();','await wakeCurrentChrome();')
outputs={'rapido.mjs':a,'ui-adb.mjs':b}
for name,txt in outputs.items():
 temp=base/(name+'.tmp-foco.mjs')
 temp.write_text(txt)
 check=subprocess.run(['node','--check',str(temp)],capture_output=True,text=True)
 if check.returncode:
  temp.unlink(missing_ok=True)
  raise RuntimeError(name+': '+check.stderr)
backup=base/('.citas-backup-foco-'+str(int(time.time())))
backup.mkdir(mode=0o700)
for name in outputs:
 shutil.copy2(base/name,backup/name)
 (base/(name+'.tmp-foco.mjs')).replace(base/name)
print('PARCHE DE CHROME VALIDADO. Perfil y vigilancia intactos.')
