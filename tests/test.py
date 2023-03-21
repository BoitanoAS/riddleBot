import base64
import json


def tests():
    test = [{'dag_0': 'True'}, {'dag_0': 'False'}, {'dag_0': 'False'}, {}, {'dag_0': 'True'}]
    count = 0
    t_sum = [count + 1 for x in test if x.get('dag_0') == 'True']
    print(sum(t_sum))
    new_text_arr = ["dag_a", "ans"]
    is_int = int(new_text_arr[0][-1])
    print(is_int)


if __name__ == '__main__':
    str_n64 = "cGF5bG9hZD0lN0IlMjJ0eXBlJTIyJTNBJTIyc2hvcnRjdXQlMjIlMkMlMjJ0b2tlbiUyMiUzQSUyMmpKOGFGS1dpYkRkZkZKdHc3eUloTjg2bSUyMiUyQyUyMmFjdGlvbl90cyUyMiUzQSUyMjE2Nzk0MDA3NzUuMjkzMTU1JTIyJTJDJTIydGVhbSUyMiUzQSU3QiUyMmlkJTIyJTNBJTIyVDA0UVBQS0RXUFIlMjIlMkMlMjJkb21haW4lMjIlM0ElMjJtYXVydGVzdCUyMiU3RCUyQyUyMnVzZXIlMjIlM0ElN0IlMjJpZCUyMiUzQSUyMlUwNFJVME5UTkdHJTIyJTJDJTIydXNlcm5hbWUlMjIlM0ElMjJtYXVyZWVuJTIyJTJDJTIydGVhbV9pZCUyMiUzQSUyMlQwNFFQUEtEV1BSJTIyJTdEJTJDJTIyaXNfZW50ZXJwcmlzZV9pbnN0YWxsJTIyJTNBZmFsc2UlMkMlMjJlbnRlcnByaXNlJTIyJTNBbnVsbCUyQyUyMmNhbGxiYWNrX2lkJTIyJTNBJTIycG9lbmd0YXZsZSUyMiUyQyUyMnRyaWdnZXJfaWQlMjIlM0ElMjI0OTgwOTEyNjIzMzk3LjQ4Mzk4MDE0NzI4MDcuODllNThlNmExNGNiNmY3OWU3ZmY0ZDgwMjhkZjA5ODMlMjIlN0Q="
    admins = ["U04RU0NTNGG", "U04RR7JBZ0V", "U04RMH9SPV4"]
    tst_dct = base64.b64decode(str_n64).decode("ascii").replace("%22", '"').replace("%3A", ":").replace("%2C", ",").replace("%7B", "{").replace("%7D", "}").replace("payload=", "")
    inputs = json.loads(tst_dct)
    print(inputs)
    user_id = inputs.get("user").get("id")
    if user_id in admins:
        print("doew")

