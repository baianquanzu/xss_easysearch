#!/usr/bin/env python3
import subprocess
import sys

def run_commands(domain):
    try:
        # 1. ���� subfinder
        print("[*] �������� subfinder...")
        subfinder_cmd = f"subfinder -d all {domain} | tee 2.{domain}.txt"
        subprocess.run(subfinder_cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[+] subfinder ���")

        # 2. �ϲ��ļ��� out.txt (ֻʹ�� subfinder ���ɵ��ļ�)
        print("[*] ���ںϲ��ļ��� out.txt...")
        merge_cmd = f"cat 2.{domain}.txt | sort -u >> out.txt"
        subprocess.run(merge_cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[+] �ϲ����")

        # 3. ���� waybackurls ��д�� e1.txt
        print("[*] �������� waybackurls ��д�� e1.txt...")
        waybackurls_cmd = "cat out.txt | waybackurls | sort -u >> e1.txt"
        subprocess.run(waybackurls_cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[+] waybackurls ���")

        # 4. ȥ�������ļ���д�� end.txt
        print("[*] ����ȥ�ز�д�� end.txt...")
        dedup_cmd = r'cat e1.txt | egrep -iv "\.(jpg|swf|mp3|mp4|m3u8|ts|jpeg|gif|css|tif|tiff|png|ttf|woff|woff2|ico|pdf|svg|txt|js)" | tee end.txt'
        subprocess.run(dedup_cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[+] ȥ�����")

        # 5. ���� xscan �� end.txt ���ݽ���ɨ��
        print("[*] �������� xscan ɨ�� end.txt...")
        xscan_cmd = "./xscan spider -f end.txt"
        subprocess.run(xscan_cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[+] xscan ɨ�����")

    except subprocess.CalledProcessError as e:
        print(f"[!] ����ִ��ʧ��: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 all.py <domain>")
        sys.exit(1)

    domain = sys.argv[1]
    run_commands(domain)

