#!/usr/bin/env python3
import subprocess
import sys

def run_commands(domain):
    try:
        # 1. 运行 subfinder
        print("[*] 正在运行 subfinder...")
        subfinder_cmd = f"subfinder -d all {domain} | tee 2.{domain}.txt"
        subprocess.run(subfinder_cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[+] subfinder 完成")

        # 2. 合并文件到 out.txt (只使用 subfinder 生成的文件)
        print("[*] 正在合并文件到 out.txt...")
        merge_cmd = f"cat 2.{domain}.txt | sort -u >> out.txt"
        subprocess.run(merge_cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[+] 合并完成")

        # 3. 运行 waybackurls 并写入 e1.txt
        print("[*] 正在运行 waybackurls 并写入 e1.txt...")
        waybackurls_cmd = "cat out.txt | waybackurls | sort -u >> e1.txt"
        subprocess.run(waybackurls_cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[+] waybackurls 完成")

        # 4. 去重无用文件并写入 end.txt
        print("[*] 正在去重并写入 end.txt...")
        dedup_cmd = r'cat e1.txt | egrep -iv "\.(jpg|swf|mp3|mp4|m3u8|ts|jpeg|gif|css|tif|tiff|png|ttf|woff|woff2|ico|pdf|svg|txt|js)" | tee end.txt'
        subprocess.run(dedup_cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[+] 去重完成")

        # 5. 运行 xscan 对 end.txt 内容进行扫描
        print("[*] 正在运行 xscan 扫描 end.txt...")
        xscan_cmd = "./xscan spider -f end.txt"
        subprocess.run(xscan_cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[+] xscan 扫描完成")

    except subprocess.CalledProcessError as e:
        print(f"[!] 命令执行失败: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 all.py <domain>")
        sys.exit(1)

    domain = sys.argv[1]
    run_commands(domain)

