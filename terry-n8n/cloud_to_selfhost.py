import requests, sys

SRC_BASE = "https://tshelton.app.n8n.cloud"
DST_BASE = "https://n8n.srv993714.hstgr.cloud"
API_VER  = "v1"
SRC_KEY  = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwZmUyODIwNy02ZWVhLTQzNTktYmQ2MS1lMDcwYmU5ZDNlNGEiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzU3MDUwOTQ4LCJleHAiOjE3NTk2MzY4MDB9.jo7mNCozuH_sp9-ORGrXBT6T1KQ_XjHCA61HJtr6qSs"
DST_KEY  = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwODZiYzRlMC0xZTZkLTQwMGEtYjg4OS1jNWMyNWUxZDZhOTUiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzU3MDUwOTc5LCJleHAiOjE3NTk2MTUyMDB9._kcGlT5GQ7xxPFrTsUdCcILx8erVJOPFrIjKniCNrhI"

sh = requests.Session()
dh = requests.Session()
sh.headers.update({"X-N8N-API-KEY": SRC_KEY})
dh.headers.update({"X-N8N-API-KEY": DST_KEY})

def list_workflows(base, sess):
    r = sess.get(f"{base}/api/workflows", params={"limit": 9999})
    r.raise_for_status()
    return r.json()["data"]

def get_workflow(base, sess, wf_id):
    r = sess.get(f"{base}/api/workflows/{wf_id}")
    r.raise_for_status()
    return r.json()

def find_by_name(base, sess, name):
    r = sess.get(f"{base}/api/workflows", params={"limit": 9999})
    r.raise_for_status()
    for wf in r.json()["data"]:
        if wf["name"] == name:
            return wf["id"]
    return None

def upsert_workflow(dst_base, dst_sess, wf):
    name = wf["name"]
    # Keep commonly accepted fields
    payload = {
        "name": name,
        "nodes": wf.get("nodes", []),
        "connections": wf.get("connections", {}),
        "settings": wf.get("settings", {}),
        "tags": wf.get("tags", []),
        "active": wf.get("active", False),
    }
    existing_id = find_by_name(dst_base, dst_sess, name)
    if existing_id:
        r = dst_sess.put(f"{dst_base}/api/workflows/{existing_id}", json=payload)
        r.raise_for_status()
        print(f"Updated: {name} (id {existing_id})")
    else:
        r = dst_sess.post(f"{dst_base}/api/workflows", json=payload)
        r.raise_for_status()
        print(f"Created: {name}")

def main():
    src_wfs = list_workflows(SRC_BASE, sh)
    for wf in src_wfs:
        full = get_workflow(SRC_BASE, sh, wf["id"])
        upsert_workflow(DST_BASE, dh, full)
    print("Done. All workflows mirrored (structure & nodes).")

if __name__ == "__main__":
    sys.exit(main())
