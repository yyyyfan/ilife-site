import os,re,json,base64,mimetypes,blake3,requests
jwt=re.search(r'"jwt": "([^"]+)"',open(__import__('sys').argv[1]).read())[1]
H={'Authorization':'Bearer '+jwt};A='https://api.cloudflare.com/client/v4/pages/assets/'
root=os.environ.get('SITE_ROOT','ilife-site');files={}
for d,ds,fs in os.walk(root):
    ds[:]=[x for x in ds if x not in('.git','db')]
    for f in fs:
        p=os.path.join(d,f);b=base64.b64encode(open(p,'rb').read()).decode()
        ext=os.path.splitext(f)[1][1:]
        h=blake3.blake3((b+ext).encode()).hexdigest()[:32]
        files['/'+os.path.relpath(p,root)]=(h,p,b)
man={k:v[0] for k,v in files.items()};json.dump(man,open(os.environ.get('MANIFEST','cf_manifest.json'),'w'))
hashes=list({v[0] for v in files.values()})
r=requests.post(A+'check-missing',headers=H,json={'hashes':hashes}).json();miss=set(r['result'])
print(len(files),'missing',len(miss))
byh={v[0]:v for v in files.values()};batch=[];size=0
def send(b):
    rr=requests.post(A+'upload',headers=H,json=b,timeout=300);assert rr.ok,rr.text[:300]
for h in miss:
    _,p,b=byh[h];batch.append({'key':h,'value':b,'metadata':{'contentType':mimetypes.guess_type(p)[0] or 'application/octet-stream'},'base64':True});size+=len(b)
    if size>30e6 or len(batch)>=1000: send(batch);batch=[];size=0
if batch: send(batch)
print(requests.post(A+'upsert-hashes',headers=H,json={'hashes':hashes}).json().get('success'))
