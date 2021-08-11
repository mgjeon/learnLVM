import time
import threading

def find_users_sync(n):
    for i in range(1, n+1):
        print(f'{n}명 중 {i}번 째 사용자 조회 중 ...')
        time.sleep(1)
    print(f'> 총 {n}명 사용자 동기 조회 완료!')


def process_thread():
    threading.Thread(target=find_users_sync, args=(3,)).start()
    threading.Thread(target=find_users_sync, args=(2,)).start()
    threading.Thread(target=find_users_sync, args=(1,)).start()

if __name__ == '__main__':
    process_thread()
    