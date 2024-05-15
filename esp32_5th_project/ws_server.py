import socket as s
ADDR = ("127.0.0.1",8080)
SIZE = 1024
FORMAT = "utf-8"

def main():
	print("Start")
	client = s.socket(s.AF_INET,s.SOCK_STREAM)
	client.connect(ADDR)
	print("CONNECTED")
	while(True):
		data = client.recv(SIZE).decode(FORMAT)
		print(data)
		client.send(data.encode(FORMAT))
	client.close()
	
if __name__ == "__main__":
	main()