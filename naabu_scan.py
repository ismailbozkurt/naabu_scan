from time import sleep

import docker

client = docker.from_env()


def check_image_exist(image_tag):
    try:
        updated_tag = image_tag + ":latest"
        image_list = client.images.list()
        if len(image_list) != 0:
            for image in image_list:
                exist_tag = image.tags[0]
                if updated_tag == exist_tag:
                    return True
        return False
    except Exception as err:
        raise err


def build_image(dockerfile_path, dockerfile_name, image_tag):
    try:
        print("build executed")
        client.images.build(path=dockerfile_path, dockerfile=dockerfile_name, tag=image_tag, forcerm=True)
        return True
    except Exception as err:
        print(err)
        return False


def force_installation_dockers(image_tag_list):
    for image_dict in image_tag_list:
        if check_image_exist(image_dict["image_tag"]) is False:
            print(image_dict["image_tag"])
            while True:
                if build_image(image_dict["path"], image_dict["dockerfile"], image_dict["image_tag"]):
                    print("build successfully on {0}".format(image_dict["image_tag"]))
                    break
                else:
                    print("on_sleep")
                    sleep(45)
        else:
            print("image exist installation skipped")
            return True
    return True


def naabu_host_exec(local_client, domain_name, image_tag):
    try:
        resp = local_client.containers.run(image_tag,
                                     ["-host", domain_name,
                                      "-p", "8080,10000,20000,2222,7080,9009,7443,2087,2096,8443,4100,2082,2083,2086,9999,2052,9001,9002,7000,7001,8082,8084,8085,8010,9000,2078,2080,2079,2053,2095,4000,5280,8888,9443,5800,631,8000,8008,8087,84,85,86,88,10125,9003,7071,8383,7547,3434,10443,8089,3004,81,4567,7081,82,444,1935,3000,9998,4433,4431,4443,83,90,8001,8099,80,300,443,591,593,832,981,1010,1311,2480,3128,3333,4243,4711,4712,4993,5000,5104,5108,6543,7396,7474,8014,8042,8069,8081,8088,8090,8091,8118,8123,8172,8222,8243,8280,8281,8333,8500,8834,8880,8983,9043,9060,9080,9090,9091,9200,9800,9981,12443,16080,18091,18092,20720,28017,6060",
                                      "-json",
                                      "-o", "/dev/shm/out_host_naabu.txt"],
                                     volumes={
                                         '/tmp/naabu_scan': {
                                             'bind': '/dev/shm', 'mode': 'rw'}},
                                     auto_remove=True)
        print(resp)
        return resp

    except Exception as err:
        raise err

#
# def naabu_ip_exec(local_client, ip_addr_or_range, image_tag): try: resp = local_client.containers.run(image_tag,
# ["-nmap-cli", "'nmap {0}-sV -oX /dev/shm/out_nmap'".format(ip_addr_or_range), # "-p", "8080,10000,20000,2222,7080,
# 9009,7443,2087,2096,8443,4100,2082,2083,2086,9999,2052,9001,9002,7000,7001,8082,8084,8085,8010,9000,2078,2080,2079,
# 2053,2095,4000,5280,8888,9443,5800,631,8000,8008,8087,84,85,86,88,10125,9003,7071,8383,7547,3434,10443,8089,3004,
# 81,4567,7081,82,444,1935,3000,9998,4433,4431,4443,83,90,8001,8099,80,300,443,591,593,832,981,1010,1311,2480,3128,
# 3333,4243,4711,4712,4993,5000,5104,5108,6543,7396,7474,8014,8042,8069,8081,8088,8090,8091,8118,8123,8172,8222,8243,
# 8280,8281,8333,8500,8834,8880,8983,9043,9060,9080,9090,9091,9200,9800,9981,12443,16080,18091,18092,20720,28017,
# 6060", "-json", ip_addr_or_range], volumes={ '/tmp/naabu_scan': { 'bind': '/dev/shm', 'mode': 'rw'}},
# auto_remove=True) print(resp) return resp
#
#     except Exception as err:
#         raise err


if __name__ == '__main__':
    with open("domain_to_scan.txt", "r") as f:
        domain = f.read()
    image_tag_list = [
        {'path': '.',
         "dockerfile": "Dockerfile.naabu",
         'image_tag': 'naabu'}]

    result = force_installation_dockers(image_tag_list)
    if result:
        naabu_host_exec(client, domain, "naabu")
        # naabu_ip_exec(client, "104.16.99.52", "naabu")
