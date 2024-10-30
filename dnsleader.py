import dns.resolver
import concurrent.futures
import time
import argparse
from colorama import Fore, Style, init
import random
import os
from tqdm import tqdm

# تهيئة colorama للعمل في الأنظمة غير المدعومة مثل Windows
init(autoreset=True)

# تحميل قائمة الـ DNS من ملف txt
def load_dns_list(filename):
    with open(filename, 'r') as file:
        dns_list = [line.strip() for line in file if line.strip()]
    return dns_list

# أنواع السجلات التي سيتم اختبارها
record_types = ['A', 'AAAA', 'CNAME', 'MX', 'NS', 'PTR', 'TXT', 'SRV', 'SOA', 'CAA', 'NAPTR', 'DS',
                'DNSKEY', 'RRSIG', 'TLSA', 'SPF', 'DNAME', 'LOC', 'HINFO', 'RP']

# اختبار استجابة DNS لجميع أنواع السجلات
def test_dns_server(dns_server, output_file, max_response_time):
    resolver = dns.resolver.Resolver(configure=False)  # تعطيل تحميل resolv.conf
    resolver.nameservers = [dns_server]
    response_time = float('inf')  # زمن الاستجابة الافتراضي كقيمة كبيرة

    try:
        for record_type in record_types:
            start_time = time.time()
            try:
                resolver.resolve('google.com', record_type)  # استعلام عن نوع السجل
            except dns.resolver.NXDOMAIN:
                print(f"{Fore.RED}[FAILED] {dns_server}: NXDOMAIN for {record_type}{Style.RESET_ALL}")
                return (dns_server, float('inf'))

            response_time = (time.time() - start_time) * 1000  # تحويل الوقت من ثوان إلى ميلي ثانية

            # حفظ الخوادم التي تكون استجابتها أقل من القيمة المحددة
            if response_time < max_response_time:
                print(f"{Fore.GREEN}[SUCCESS] {dns_server} ({record_type}): Response time: {response_time:.2f} ms{Style.RESET_ALL}")
                with open(output_file, 'a') as file:  # فتح الملف في وضع الإلحاق
                    file.write(f"{dns_server}: {response_time:.2f} ms ({record_type})\n")
            else:
                print(f"{Fore.YELLOW}[SUCCESS] {dns_server} ({record_type}): Response time is higher than {max_response_time:.2f} ms: {response_time:.2f} ms{Style.RESET_ALL}")
    except dns.resolver.NoAnswer:
        print(f"{Fore.RED}[FAILED] {dns_server}: No answer for {record_type}{Style.RESET_ALL}")
    except (dns.resolver.NoNameservers, dns.resolver.Timeout):
        print(f"{Fore.RED}[FAILED] {dns_server}: Timeout or No response{Style.RESET_ALL}")

    return (dns_server, response_time if response_time < max_response_time else float('inf'))

# فحص جميع الخوادم باستخدام multi-threading
def check_all_dns_servers(dns_list, output_file, max_response_time):
    # نستخدم ThreadPoolExecutor لتنفيذ الفحص بسرعة عبر الـ threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=300) as executor:
        # تمرير ملف الإخراج إلى كل وظيفة في الـ thread
        results = list(executor.map(lambda dns: test_dns_server(dns, output_file, max_response_time), dns_list))
    return results

def matrix_rain(duration=3):
    code_words = [
        "hack", "exploit", "system", "breach", "access", "root", "admin", "shell", "inject",
        "#!/bin/bash", "chmod 777", "/etc/shadow", "/etc/passwd", "rm -rf /*", "sudo su",
        "while true;", "for i in range()", "def hack():", "import socket", "import sys",
        "buffer = '\\x41'", "print(hex())", "0xFFFF", "127.0.0.1", "PORT=443", "DNS_HACK",
        "<script>", "alert(1)", "root:x:0:0", ".php?id=1'", "SELECT * FROM", "AND 1=1--",
        "TCP/IP", "UDP/53", "HTTP/1.1", "SSH-2.0", "GET /admin", "POST /data", "XSS",
    ]
    
    colors = [Fore.GREEN, Fore.CYAN, Fore.RED]
    width = os.get_terminal_size().columns
    height = os.get_terminal_size().lines - 5
    
    # Initialize active_words list
    active_words = []
    
    start_time = time.time()
    while (time.time() - start_time) < duration:
        print('\033[H', end='')  # Move cursor to top
        
        # Add new words
        if random.random() < 3:
            word = random.choice(code_words)
            color = random.choice(colors)
            x = random.randint(0, width - len(word))
            active_words.append({
                'word': word,
                'color': color,
                'x': x,
                'y': 0,
                'speed': random.uniform(1.5, 3.0) 
            })
        
        # Create empty screen
        screen = [[' ' for _ in range(width)] for _ in range(height)]
        
        # Update word positions and print them
        new_active_words = []
        for word_data in active_words:
            if word_data['y'] < height:
                # Print word vertically
                for i, char in enumerate(word_data['word']):
                    if int(word_data['y']) + i < height:
                        screen[int(word_data['y']) + i][word_data['x']] = f"{word_data['color']}{char}{Style.RESET_ALL}"
                word_data['speed'] *= 1.1  # Gradual acceleration
                word_data['y'] += word_data['speed']
                new_active_words.append(word_data)
        
        active_words = new_active_words
        
        # Print screen
        for row in screen:
            print(''.join(row))
        
        time.sleep(0.1)
    
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = f"""{Fore.RED}
    {Fore.GREEN}
    ▓█████▄  ███▄    █   ██████      ██░ ██  █    ██  ███▄    █ ▄▄▄█████▓▓█████  ██▀███  
    ▒██▀ ██▌ ██ ▀█   █ ▒██    ▒     ▓██░ ██▒ ██  ▓██▒ ██ ▀█   █ ▓  ██▒ ▓▒▓█   ▀ ▓██ ▒ ██▒
    ░██   █▌▓██  ▀█ ██▒░ ▓██▄       ▒██▀▀██░▓██  ▒██░▓██  ▀█ ██▒▒ ▓██░ ▒░▒███   ▓██ ░▄█ ▒
    ░▓█▄   ▌▓██▒  ▐▌██▒  ▒   ██▒    ░▓█ ░██ ▓▓█  ░██░▓██▒  ▐▌██▒░ ▓██▓ ░ ▒▓█  ▄ ▒██▀▀█▄  
    ░▒████▓ ▒██░   ▓██░▒██████▒▒    ░▓█▒░██▓▒▒█████▓ ▒██░   ▓██░  ▒██▒ ░ ░▒████▒░██▓ ▒██▒
     ▒▒▓  ▒ ░ ▒░   ▒ ▒ ▒ ▒▓▒ ▒ ░     ▒ ░░▒░▒░▒▓▒ ▒ ▒ ░ ▒░   ▒ ▒   ▒ ░░   ░░ ▒░ ░░ ▒▓ ░▒▓░
     ░ ▒  ▒ ░ ░░   ░ ▒░░ ░▒  ░ ░     ▒ ░▒░ ░░░▒░ ░ ░ ░ ░░   ░ ▒░    ░     ░ ░  ░  ░▒ ░ ▒░
     ░ ░  ░    ░   ░ ░ ░  ░  ░       ░  ░░ ░ ░░░ ░ ░    ░   ░ ░   ░         ░     ░░   ░ 
       ░             ░       ░       ░  ░  ░   ░              ░             ░  ░   ░     
     ░                                                                                    
    {Style.RESET_ALL}
    {Fore.CYAN}╔═══════════════════════════[ SYSTEM STATUS ]════════════════════════╗{Style.RESET_ALL}
    {Fore.CYAN}║{Style.RESET_ALL} {Fore.RED}[☣️] QUANTUM MATRIX INITIALIZED | CYBER WARFARE READY{Style.RESET_ALL}           {Fore.CYAN}║{Style.RESET_ALL}
    {Fore.CYAN}║{Style.RESET_ALL} {Fore.GREEN}[🧬] NEURAL NETWORK: ACTIVATED | THREAT LEVEL: MAXIMUM{Style.RESET_ALL}       {Fore.CYAN}║{Style.RESET_ALL}
    {Fore.CYAN}║{Style.RESET_ALL} {Fore.BLUE}[🌐] GLOBAL DNS INFILTRATION SYSTEM: OPERATIONAL{Style.RESET_ALL}             {Fore.CYAN}║{Style.RESET_ALL}
    {Fore.CYAN}╚═══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}

    {Fore.RED}[⚡] {Fore.YELLOW}DNS EXPLOITATION ARSENAL: {len(record_types)} VECTORS LOADED{Style.RESET_ALL}
    {Fore.RED}[🎯] {Fore.YELLOW}TARGET ACQUISITION MODE: ACTIVE{Style.RESET_ALL}
    {Fore.RED}[💀] {Fore.YELLOW}CYBER KILL CHAIN: INITIATED{Style.RESET_ALL}
    
    {Fore.GREEN}Created By {Fore.GREEN}BOOND{Style.RESET_ALL}
    """
    print(banner)

def initialize_system():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Fore.RED}[!] INITIALIZING QUANTUM CYBER WARFARE SYSTEMS...{Style.RESET_ALL}")
    
    # شريط تقدم بسيط
    bar_width = 50
    for i in range(bar_width + 1):
        progress = "█" * i + "░" * (bar_width - i)
        percentage = (i * 100) // bar_width
        print(f"\r{Fore.RED}[☢️] Loading: |{Fore.GREEN}{progress}{Fore.RED}| {percentage}%{Style.RESET_ALL}", end="")
        time.sleep(0.1)
    print("\n")
            
    os.system('cls' if os.name == 'nt' else 'clear')
    matrix_rain()
    print_banner()

# تنفيذ العملية
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DNS Tester")
    parser.add_argument("dns_file", help="The input file containing DNS servers")
    parser.add_argument("-o", "--output", help="The output file to save successful DNS servers", default="dns_results.txt")
    parser.add_argument("--max-response-time", type=float, help="Maximum allowed response time (in ms)", default=103.19)

    args = parser.parse_args()

    initialize_system()

    dns_file = args.dns_file  # اسم ملف TXT الذي يحتوي على عناوين DNS
    output_file = args.output  # ملف لحفظ النتائج
    max_response_time = args.max_response_time  # الحد الأقصى لزمن الاستجابة

    dns_list = load_dns_list(dns_file)
    
    # إضافة تأثير التحميل قبل طباعة الرسالة
    print(f"{Fore.CYAN}[*] Calculating DNS targets...{Style.RESET_ALL}")
    for _ in range(3):
        for char in "|/-\\":
            print(f"\r{Fore.YELLOW}[{char}] Processing...{Style.RESET_ALL}", end="")
            time.sleep(0.25)
    print("\r", end="")
    
    print(f"{Fore.GREEN}[✓] {Fore.WHITE}Loaded {Fore.RED}{len(dns_list)}{Fore.WHITE} DNS servers for testing with a max response time of {Fore.RED}{max_response_time}{Fore.WHITE} ms.{Style.RESET_ALL}")

    # تمرير ملف الإخراج وقيمة max_response_time
    results = check_all_dns_servers(dns_list, output_file, max_response_time)

    print(f"Results saved to {output_file}")
