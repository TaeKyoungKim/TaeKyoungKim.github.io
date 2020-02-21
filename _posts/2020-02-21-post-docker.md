# 만들면서 이해하는 도커(Docker) 이미지의 구조도커 이미지 빌드 원리와 Overayfs

[nacyot](https://www.44bits.io/ko/author/nacyot) 작성, 2019년 12월 24일 공개

[들어가며](https://www.44bits.io/ko/post/how-docker-image-work#들어가며)[도커 이미지는 어디에서 오나요?: 도커 허브(Docker Hub)](https://www.44bits.io/ko/post/how-docker-image-work#도커-이미지는-어디에서-오나요-도커-허브docker-hub)[풀 받은 도커 이미지는 어디에 저장되나요?](https://www.44bits.io/ko/post/how-docker-image-work#풀-받은-도커-이미지는-어디에-저장되나요)[특정 레이어에서 컨테이너를 실행할 수 없을까?](https://www.44bits.io/ko/post/how-docker-image-work#특정-레이어에서-컨테이너를-실행할-수-없을까)[컨테이너의 레이어 계층 이해하기](https://www.44bits.io/ko/post/how-docker-image-work#컨테이너의-레이어-계층-이해하기)[docker diff와 docker commit으로 이미지 만들기](https://www.44bits.io/ko/post/how-docker-image-work#docker-diff와-docker-commit으로-이미지-만들기)[도커 커밋으로 이미지 만들기, Dockerfile로 이미지 만들기](https://www.44bits.io/ko/post/how-docker-image-work#도커-커밋으로-이미지-만들기-dockerfile로-이미지-만들기)[이미지 직접 빌드하고 중간 레이어에서 컨테이너 실행하기](https://www.44bits.io/ko/post/how-docker-image-work#이미지-직접-빌드하고-중간-레이어에서-컨테이너-실행하기)[OverlayFS 직접 사용해보고, 임의의 위치에 도커 이미지 마운트하기](https://www.44bits.io/ko/post/how-docker-image-work#overlayfs-직접-사용해보고-임의의-위치에-도커-이미지-마운트하기)[마치며](https://www.44bits.io/ko/post/how-docker-image-work#마치며)

[**stdout.fm:** 프로그래머들의 수다 팟캐스트. 클라우드, 개발, 테크 뉴스, 전자 제품.](https://stdout.fm/)

## 들어가며

[도커](https://www.docker.com/)Docker는 컨테이너를 실행하고 관리할 수 있도록 도와주는 도구입니다. 44bits에서도 여러 번 도커(Docker)와 컨테이너 기술에 대해서 소개한 바 있습니다. 도커 기초에 대해서는 아래 글들을 참고해주세요.

- [도커(Docker) 튜토리얼 : 깐 김에 배포까지](https://www.44bits.io/ko/post/easy-deploy-with-docker)
- [왜 굳이 도커(컨테이너)를 써야 하나요? - 컨테이너를 사용해야 하는 이유 | 44bits.io](https://www.44bits.io/ko/post/why-should-i-use-docker-container)

오늘은 도커 이미지에 집중해보고자 합니다. 도커 이미지는 도커를 받들고 있는 중요한 기둥 중 하나입니다. 특히 도커 이전의 컨테이너 기술들에서는 **컨테이너의 환경을 완전하고 효율적으로 복원한다**는 게 상당히 어려운 일이었습니다. 도커는 파일을 계층으로 나눠서 저장할 수 있는 유니온 마운트Union mount 기술과 도커 허브Docker Hub라는 원격 저장소를 기본적으로 제공함으로써 이 문제를 해결했습니다. 도커 이미지는 도커의 간편한 인터페이스와 더불어 도커가 성공적으로 자리잡는 데 1등 공신 역할을 했습니다. 이 글에서는 도커 이미지가 어디에 저장되고, 어떤 원리로 동작하는지 살펴보고, 유니온 마운트 구현체 오버레이FS를 사용해서 직접 도커 이미지를 마운트하는 방법을 소개하고자 합니다.

## 도커 이미지는 어디에서 오나요?: 도커 허브(Docker Hub)

도커 이미지를 풀 받아오는 간단한 경우를 생각해보겠습니다. 다음 명령어로 `nginx:latest` 이미지를 풀 받아옵니다.

```powershell
$ docker pull nginx:latest
latest: Pulling from library/nginx
000eee12ec04: Pull complete
eb22865337de: Pull complete
bee5d581ef8b: Pull complete
Digest: sha256:50cf965a6e08ec5784009d0fccb380fc479826b6e0e65684d9879170a9df8566
Status: Downloaded newer image for nginx:latest
docker.io/library/nginx:latest
```

```
docker.io/library/nginx:latest
```

이미지를 풀 받을 때는 분명히 `nginx:latest`라는 이미지를 요청했습니다만, 풀 받아진 이미지의 이름은 `docker.io/library/nginx:latest`입니다. 둘은 사실 같은 이름입니다.

도커의 이미지 이름은 단순한 문자열입니다만, 도커 레지스트리에서 내부적으로는 파싱되어 사용됩니다. 도커 허브를 기준으로 도커 이미지 이름은 `/:` 형식으로 구성됩니다. 그래서 `nginx:latest`의 좀 더 정확한 이름은 `library/nginx:latest`입니다. 여기서 `library`는 도커 허브의 공식 이미지가 저장되어있는 특별한 네임스페이스입니다. 보통은 이 자리에 사용자의 이름이 옵니다.

네임스페이스 앞에는 슬래시로 구분된 도메인이 들어갈 수 있는데, 이 경우 도커 이미지 저장소(레지스트리)의 주소를 가리킵니다. `docker.io/library/nginx:latest` 이미지에서 `docker.io`는 이미지 저장소의 실제 주소를 가리킵니다. 여기에 도커의 아주 중요한 비밀이 숨겨져있습니다. `nginx:latest`라는 이름으로 이미지를 풀 받는 게 가능한 이유는 도커 클라이언트의 기본 도커 레지스트리가 바로 [도커 허브](https://hub.docker.com/)(`docker.io`)이기 때문입니다. 이는 `docker info` 명령으로 확인해볼 수 있습니다.

```powershell
$ docker info
...
 Registry: https://index.docker.io/v1/
 Labels:
 Experimental: false
 Insecure Registries:
  127.0.0.0/8
 Live Restore Enabled: false
 Product License: Community Engine
```

출력 결과의 가장 아래 쪽에 레지스트리Registry라는 항목이 있습니다. `docker.io`가 아니라 `https://index.docker.io/v1/`라고 되어있습니다. 약간 다르긴 합니다만, 실제로 같은 주소를 가리킵니다. 도커 인덱스는 도커 허브의 원래 이름이자 도메인입니다. 도커 이미지에서 사용할 수 있는 형식으로 주소를 바꾸면 다음과 같습니다: `index.docker.io/library/nginx:latest`.

한 가지를 더 살펴보겠습니다. 이미지를 풀 받을 때 아래 쪽에 보면 sha256 digest값이 하나 있습니다.

```powershell
sha256:50cf965a6e08ec5784009d0fccb380fc479826b6e0e65684d9879170a9df8566
```

도커 허브에서는 이 값을 가지고 이미지를 풀 받을 수도 있습니다. 따라서 글을 쓰는 시점에 (최소한) 다음 5가지 이미지 주소는 모두 같은 이미지를 가리킵니다.*****

- nginx:latest
- nginx@sha256:50cf965a6e08ec5784009d0fccb380fc479826b6e0e65684d9879170a9df8566
- library/nginx:latest
- docker.io/library/nginx:latest
- index.docker.io/library/nginx:latest

***** 여기서 같은 이미지라는 것은 도커 허브에서 ‘이미지를 풀을 받을 때’ 같다는 의미입니다. 앞서 잠깐 언급했습니다만, 도커 이미지 이름은 단순히 문자열이기 때문에 로컬 환경에서 작업할 때는 같은 이름을 가진 전혀 다른 이미지를 만드는 것도 가능합니다. 따라서 이름만으로는 결코 어떤 이미지가 ‘특정한’ 이미지임을 보장할 수 없습니다.

## 풀 받은 도커 이미지는 어디에 저장되나요?

다시 도커 이미지를 풀 받을 때 출력되는 결과를 살펴보겠습니다.

```powershell
$ docker pull nginx:latest
latest: Pulling from library/nginx
000eee12ec04: Pull complete
eb22865337de: Pull complete
bee5d581ef8b: Pull complete
Digest: sha256:50cf965a6e08ec5784009d0fccb380fc479826b6e0e65684d9879170a9df8566
Status: Downloaded newer image for nginx:latest
docker.io/library/nginx:latest
```

이번에 살펴볼 부분은 다음과 같습니다.

```powershell
000eee12ec04: Pull complete
eb22865337de: Pull complete
bee5d581ef8b: Pull complete
```

이미지를 풀 받을 때 뭔가를 나눠서 받고 있습니다. 이 한 줄 한 줄이 레이어에 해당합니다. 도커의 기본 개념을 이해하고 계신 분들이라면 도커 이미지가 레이어들로 구성된다는 것을 이미 알고 계실 겁니다.

이미지를 풀 받으면 레이어들은 독립적으로 저장됩니다. 그리고 컨테이너를 실행할 때는 이 레이어들을 차례대로 쌓아올려서 특정 위치에 마운트를 합니다. 기본적으로 이미지에 속하는 레이어들은 읽기 전용이기 때문에 **절대로 변하지 않습니다**. 그리고 그 위에 마지막으로 컨테이너 전용 쓰기 가능한 레이어를 한 층 더 쌓고, 컨테이너에서 일어나는 모든 변경 사항을 이 레이어에 저장합니다.

`nginx:latest` 이미지는 위에서 확인할 수 있듯이 총 3개의 레이어로 나뉘어져있습니다. 순서대로 제일 아래의 레이어가 000eee12ec04가 됩니다. 그 위에 차례대로 eb22865337de, bee5d581ef8b 레이어를 쌓아올리면 `nginx:latest` 이미지가 됩니다. 그렇다면 이 레이어들은 어디에 저장되어있을까요? 한 번 찾아보도록 하겠습니다.

확인한 환경은 우분투Ubuntu 18.04, 도커Docker 19.03.5입니다. 먼저 `docker info` 명령어로 현재 환경에서 사용중인 스토리지 드라이버를 확인해봅니다.

```powershell
root@ubuntu1804:~/debian# docker info | grep Storage
 Storage Driver: overlay2
```

`overlay2` 드라이버가 나오는 것을 확인할 수 있습니다. 도커는 유니온 마운트(계층화된 파일 시스템)를 지원하는 다양한 스토리지 드라이버를 지원하고 있습니다. 현재 리눅스 커널에는 Overlayfs가 포함되어있어서 이를 사용하는 경우가 많습니다.

도커의 데이터는 기본적으로 시스템 상의 `/var/lib/docker/`에 저장되며 overlay2 드라이버로 저장된 레이어 데이터는 다시 `image/overlay2/layerdb/sha256` 아래에 저장됩니다. 이 디렉터리에서 현재 시스템에 저장된 레이어들을 확인해보겠습니다.*****

***** 여기서부터는 관리자 권한으로 작업해야합니다. 실습을 하는 경우 `sudo su` 명령을 사용하거나 root 계정으로 로그인해서 진행하시기 바랍니다.

```powershell
$ pwd
/var/lib/docker/image/overlay2/layerdb/sha256
$ ls -1
77fcff986d3b13762e4777046b9210a109fda20cb261bd3bbe5d7161d4e73c8e/
831c5620387fb9efec59fc82a42b948546c6be601e3ab34a87108ecf852aa15f/
dc8adf8fa0fc82a56c32efac9d0da5f84153888317c88ab55123d9e71777bc62/
```

다이제스트 값으로 된 디렉터리 목록을 확인할 수 있습니다. 문제는 도커 이미지를 풀 할 때 출력된 000eee12ec04, eb22865337de, bee5d581ef8b 어느 하나와도 일치하지 않는다는 점입니다. 이는 이미지 ID가 한 가지가 아니기 때문에 발생하는 문제입니다. 이미지를 풀할 때 출력되는 다이제스트 값은 원격 도커 레지스트리Distribution에서 관리하는 고유한 아이디입니다. 그런데 레이어의 아이디는 또 별도로 있습니다. `docker image inspect` 명령어로 레이어 목록을 확인해보겠습니다.

```powershell
$ docker image inspect nginx | jq  '.[].RootFS'
{
  "Type": "layers",
  "Layers": [
    "sha256:831c5620387fb9efec59fc82a42b948546c6be601e3ab34a87108ecf852aa15f",
    "sha256:5fb987d2e54d85820d95d6c31f3fe4cd95bf71fe6d9d9e4684082cb551b728b0",
    "sha256:4fc1aa8003a3d0d2481f10d17773869cbff12c1008df30e0bab8259086a0311c"
  ]
}
```

여기서는 jq로 출력 결과를 필터링 했습니다. 여기서 레이어 목록을 확인해보면, 위에서 `layerdb/sha256` 아래에 있는 디렉터리 이름과 일치하는 것을 확인할 수 있습니다.

노트

디스트리뷰션 레이어 ID에 대응하는 레이어 ID 찾기

잘 찾아보면 디스트리뷰션의 레이어 ID와 레이어 ID가 맵핑되어있는 곳도 찾을 수 있습니다. `/image/overlay2/distribution/diffid-by-digest/sha256` 아래에 있는 파일의 이름은 디스트리뷰션 ID들입니다. 이 아래에 있는 파일을 출력해보면, 레이어 ID가 출력됩니다.

```powershell
$ cat 000eee12ec04cc914bf96e8f5dee7767510c2aca3816af6078bd9fbe3150920c ; echo
sha256:831c5620387fb9efec59fc82a42b948546c6be601e3ab34a87108ecf852aa15f
```

이를 통해 이미지 풀할 때 출력된 000eee12ec04는 831c5620387… 레이어에 대응하는 것을 확인할 수 있습니다. 풀 할 때 디스트리뷰션 ID가 출력되지만 이 ID 값이 사용되는 경우는 거의 없습니다.

이제 `layerdb/sha256/`에서 실제로 레이어 내용을 확인해보겠습니다.

```powershell
$ pwd
/var/lib/docker/image/overlay2/layerdb/sha256
$ cd 831c5620387fb9efec59fc82a42b948546c6be601e3ab34a87108ecf852aa15f
$ ls -1
cache-id
diff
size
tar-split.json.gz
```

여기에 레이어에 포함된 파일이 있는 것 같지는 않네요. 실제 데이터는 또 다른 곳에 있습니다. 파일 목록 중에 `cache-id`라는 파일이 있습니다. 이 값을 출력해보면 실제 데이터가 있는 디렉터리의 다이제스트 값이 출력됩니다.

```powershell
$ cat cache-id ; echo
e5b51f307392f7a3776edaa67d5d14b85e04dad9aeca753ac6ad30aaeaa55152
```

레이어 ID는 고유한 값이지만, cache-id는 고유한 값이 아니므로 이미지를 풀 받은 시스템 마다 달라집니다. 이 디렉터리는 `/var/lib/docker` 바로 아래의 `overlay2` 아래에 있습니다. 정확히는 다이제스트 이름을 가진 디렉터리 아래의 `diff` 파일에 레이어의 컨텐츠가 들어있습니다.

```powershell
$ pwd
/var/lib/docker/overlay2/
$ ls
10a07b3d72ac36291843eb6ca01698649220065d3b3046f63546fcee49c3c36f
7e5bc8d3a02343bf40d479979e734343faff52b8fc768959a24e860c30ae4b74
e5b51f307392f7a3776edaa67d5d14b85e04dad9aeca753ac6ad30aaeaa55152
l
$ cd e5b51f307392f7a3776edaa67d5d14b85e04dad9aeca753ac6ad30aaeaa55152/diff
$ ls
bin  boot  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
```

`e5b551...`은 `nginx:latest` 이미지의 베이스 이미지에 해당하는 `debian:buster-slim` 이미지입니다. 리눅스 운영체제의 기본적인 디렉터리 구성을 확인할 수 있네요. 정말 여기에 이미지의 내용이 저장되는 걸까요? 한 번 파일을 추가해서 확인해보겠습니다. 먼저 `debian:buster-slim` 이미지로 컨테이너를 실행시켜보겠습니다.

```powershell
$ docker run -it debian:buster-slim bash
root@21df6a61c090:/# ls
bin  boot  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
```

위에서 확인한 디렉터리 구조와 완전히 같은 것을 확인할 수 있습니다. 이번에는 앞서 확인

한 레이어 디렉터리에 파일을 추가하고 다시 컨테이너를 실행시켜보겠습니다.

```powershell
$ pwd
/var/lib/docker/overlay2/e5b51f307392f7a3776edaa67d5d14b85e04dad9aeca753ac6ad30aaeaa55152/diff
$ echo 'Hello, world!' > AWESOME_NEW_FILE
$ ls
AWESOME_NEW_FILE  bin  boot  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
$ docker run -it debian:buster-slim bash

root@0c44cef0fe4a:/# ls
AWESOME_NEW_FILE  bin  boot  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
root@0c44cef0fe4a:/# cat AWESOME_NEW_FILE
Hello, world!
```

놀라운 결과를 확인할 수 있습니다. 앞서 이미지의 레이어는 절대 변하지 않는다고 이야기했습니다만, 레이어도 결국 접근 가능한 파일로 구성되어있기 때문에 관리자 권한으로 파일을 변경할 경우 이러한 변경 사항들이 반영되어버립니다. 실제로 도커를 사용할 때는 절대 이런 식으로 이미지를 구성하는 레이어를 임의로 변경해서는 안 됩니다. 위의 예제에서 확인할 수 있듯이 실행단에서 레이어 컨텐츠에 대한 검증은 따로 이루어지지 않습니다. 단, 이는 로컬에 저장되어있는 레이어를 수정한 것이지, 원격의 이미지 자체를 수정한 것은 아닙니다.

## 특정 레이어에서 컨테이너를 실행할 수 없을까?

이미지는 레이어들을 차례로 쌓아올린 결과물입니다. 그렇다면 자연스럽게 다음과 같이 생각해볼 수 있습니다. **특정 레이어에서 컨테이너를 실행할 수 있지 않을까?**

훌륭한 추론입니다만, 답은 가능하기도 하고 아니기도 하고, 애매합니다. 도커 1.10 이전에는 이미지와 레이어에 거의 차이가 없었습니다. 앞서 도커 이미지의 레이어가 어떻게 저장되는지에 대해서 살펴보았습니다만, 현재 도커 최신 버전에서는 ’레이어 = 이미지’라는 공식이 성립되지 않습니다. 반복적으로 확인합니다만, 다시 `nginx:latest` 이미지를 풀 하는 예제를 살펴보겠습니다.

```powershell
$ docker pull nginx:latest
latest: Pulling from library/nginx
000eee12ec04: Pull complete
eb22865337de: Pull complete
bee5d581ef8b: Pull complete
Digest: sha256:50cf965a6e08ec5784009d0fccb380fc479826b6e0e65684d9879170a9df8566
Status: Downloaded newer image for nginx:latest
docker.io/library/nginx:latest
```

이 상태에서 `docker images` 명령어로 현재 도커 데몬에서 사용가능한 이미지 목록을 출력해봅니다. 이 때 `-a`를 붙이면 도커 빌드 중에 생성되어서 이름과 태그가 지정되지 않은 중간 이미지 목록도 확인할 수 있습니다.

```powershell
$ docker images -a
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
nginx               latest              231d40e811cd        3 weeks ago         126MB
```

`nginx:latest` 이미지 딱 하나만 나옵니다. 하지만 1.10 버전 이전에는 다음과 같이 출력되었을 것입니다.

```powershell
# docker images -a
REPOSITORY          TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
nginx               latest              bee5d581ef8b        3 weeks ago         126MB
<none>              <none>              e9a8bb928312        3 weeks ago         126MB
<none>              <none>              eb22865337de        3 weeks ago         126MB
<none>              <none>              a8222839283b        3 weeks ago         126MB
<none>              <none>              abffffe8923f        3 weeks ago         126MB
...
<none>              <none>              000eee12ec04        2 months ago        69.2MB
<none>              <none>              382b287acfab        2 months ago        69.2MB
```

차이가 보이시나요? 1.10 이전에는 레이어가 곧 이미지였기 때문에 이미지 목록에 레이어에 해당하는 이미지들이 출력되었습니다.*****

***** 이 실행결과는 직접 실행한 결과가 아닙니다. 실제 레이어 갯수나 동작이나 이미지 ID 계산 방식 등은 차이가 있을 수 있습니다.

크게 두 가지 차이점이 있습니다. 하나는 레이어가 이미지로 출력된다는 점과 레이어의 갯수가 풀 받을 때보다 많다는 점입니다. 먼저 레이어가 이미지 ID를 가지고 있기 때문에 이를 사용해 컨테이너를 실행하는 것이 가능했습니다. 하지만 지금은 도커 이미지를 풀 받을 때 레이어는 레이어로 남겨두고 최종 레이어를 기반으로 한 이미지만을 이미지로 사용할 수 있습니다. 따라서 현재는 풀 받은 이미지의 중간 레이어로 컨테이너를 실행시키는 것이 (불가능하지는 않지만) 쉽지 않습니다.

이미지 갯수는 왜 다른 걸까요? 이는 `docker hisotry` 명령어로 이유를 찾아볼 수 있습니다. docker history는 이미지가 만들어지기 까지의 과정 전체를 보여주는 명령어입니다.

```powershell
$ docker history nginx:latest
IMAGE               CREATED             CREATED BY                                      SIZE                COMMENT
231d40e811cd        3 weeks ago         /bin/sh -c #(nop)  CMD ["nginx" "-g" "daemon.   0B
<missing>           3 weeks ago         /bin/sh -c #(nop)  STOPSIGNAL SIGTERM           0B
<missing>           3 weeks ago         /bin/sh -c #(nop)  EXPOSE 80                    0B
<missing>           3 weeks ago         /bin/sh -c ln -sf /dev/stdout /var/log/nginx.   22B
<missing>           3 weeks ago         /bin/sh -c set -x     && addgroup --system -.   57.1MB
<missing>           3 weeks ago         /bin/sh -c #(nop)  ENV PKG_RELEASE=1~buster     0B
<missing>           3 weeks ago         /bin/sh -c #(nop)  ENV NJS_VERSION=0.3.7        0B
<missing>           3 weeks ago         /bin/sh -c #(nop)  ENV NGINX_VERSION=1.17.6     0B
<missing>           3 weeks ago         /bin/sh -c #(nop)  LABEL maintainer=NGINX Do.   0B
<missing>           3 weeks ago         /bin/sh -c #(nop)  CMD ["bash"]                 0B
<missing>           3 weeks ago         /bin/sh -c #(nop) ADD file:bc8179c87c8dbb3d9.   69.2MB
```

`Dockerfile`을 작성해본 적이 있다면 결과값에 보이는 내용이 도커 파일로 이미지를 빌드한 과정이라는 것을 어렴풋이 알아보실 겁니다. 이 이미지는 베이스 이미지를 포함해 총 11단계의 명령어로 작성되었습니다. 예전에는 11단계 모든 단계가 레이어로 다뤄졌습니다만, 현재는 이미지에 메타데이터로 저장되는 부분은 레이어로 다뤄지지 않습니다. 따라서 현재는 CMD, LABEL, ENV, EXPOSE, STOPSINAL과 같은 메타데이터를 다루는 부분은 레이어로 저장되지 않고, ADD나 RUN이 일어나는 3단계만이 레이어로 저장됩니다. 이는 풀 받을 때 출력되는 레이어 갯수와 일치합니다. (달리 말하면 예전에는 같은 이미지에 대해서 더 많은 레이어를 받아왔을 것입니다.)

`histroy`의 출력 결과에서도 알 수 있습니다만 중간 레이어들의 이미지 ID 값은 `` 상태입니다. 따라서 중간 레이어로 컨테이너를 실행할 수 없습니다. 그렇다고 아예 방법이 없는 건 아닌데, 중간 레이어에서 컨테이너를 실행하기 위해서는 현재 머신에 직접 도커 빌드를 수행해야합니다. 이 방법에 대해서는 도커 이미지를 직접 한땀한땀 만들어보고, 다시 이야기하도록 하겠습니다.

노트

도커 1.10 이전과 이후의 이미지 ID

1.10 이전과 이후의 이미지 ID 다루는 방식의 변화에 대해서 관심이 있다면 이래 글들을 추천드립니다.

- [1.10 Distribution Changes Design Doc](https://gist.github.com/aaronlehmann/b42a2eaf633fc949f93b)
- [117. [Docker\] Docker에서 이미.. : 네이버블로그](https://blog.naver.com/alice_k106/221149596996)

## 컨테이너의 레이어 계층 이해하기

도커 이미지가 어떻게 만들어지는지 이해하려면 먼저 컨테이너의 레이어 구조에 대해서 이야기해야합니다. 컨테이너를 사용해보셨다면 귀에 못이 박히도록 도커는 계층화된 파일 시스템을 이용하고, 이미지는 불변이라는 얘기를 들어오셨을 겁니다. 그럼 여기서는 실제로 컨테이너를 실행핬을 때 레이어 계층이 어떻게 구성되는지 살펴보겠습니다.

```powershell
$ docker history nginx:latest
IMAGE               CREATED             CREATED BY                                      SIZE                COMMENT
231d40e811cd        3 weeks ago         /bin/sh -c #(nop)  CMD ["nginx" "-g" "daemon.   0B
<missing>           3 weeks ago         /bin/sh -c #(nop)  STOPSIGNAL SIGTERM           0B
<missing>           3 weeks ago         /bin/sh -c #(nop)  EXPOSE 80                    0B
<missing>           3 weeks ago         /bin/sh -c ln -sf /dev/stdout /var/log/nginx.   22B
<missing>           3 weeks ago         /bin/sh -c set -x     && addgroup --system -.   57.1MB
<missing>           3 weeks ago         /bin/sh -c #(nop)  ENV PKG_RELEASE=1~buster     0B
<missing>           3 weeks ago         /bin/sh -c #(nop)  ENV NJS_VERSION=0.3.7        0B
<missing>           3 weeks ago         /bin/sh -c #(nop)  ENV NGINX_VERSION=1.17.6     0B
<missing>           3 weeks ago         /bin/sh -c #(nop)  LABEL maintainer=NGINX Do.   0B
<missing>           3 weeks ago         /bin/sh -c #(nop)  CMD ["bash"]                 0B
<missing>           3 weeks ago         /bin/sh -c #(nop) ADD file:bc8179c87c8dbb3d9.   69.2MB
```

이 중에서 실제로 레이어로 사용되는 3줄만 남기고 이름을 붙여보겠습니다.

```powershell
nginx-layer3           3 weeks ago         /bin/sh -c ln -sf /dev/stdout /var/log/nginx.   22B
nginx-layer2           3 weeks ago         /bin/sh -c set -x     && addgroup --system -.   57.1MB
nginx-layer1           3 weeks ago         /bin/sh -c #(nop) ADD file:bc8179c87c8dbb3d9.   69.2MB
```

레이어는 아래에서부터 위로 쌓아올라갑니다. 따라서 layer1이 바닥에 있고, 그 위에 layer2가 올라가고 마지막으로 layer3가 위에 올라가서 비로소 이미지가 됩니다. 그리고 다시 한 번 이야기하지만, 이미지의 레이어들은 모든 읽기 전용입니다. 컨테이너에서 무슨 짓을 하더라도 절대로 이미지의 내용이 달라지지 않습니다.

```powershell
nginx-layer3(RO) = nginx:latest
nginx-layer2(RO)
nginx-layer1(RO)
```

유니온 마운트를 이해하지 못 하더라도 일단 레이어들을 쌓아서 이미지가 만들어진다는 느낌은 오셨을 겁니다. 여기서 등장하는 게 컨테이너입니다. 그럼 대체 컨테이너를 실행하면 무슨 일이 벌어지는 걸까요? 답은 간단합니다. 컨테이너를 실행할 때 아주 깨끗한 레이어를 하나 이미지의 최상위 레이어 위에 올려줍니다. 컨테이너를 한 대 실행시켜보겠습니다.

```powershell
$ docker run -it nginx:latest bash
root@34a6aa18a83c:/#
```

방금 생성한 컨테이너 아이디(호스트네임)는 34a6aa18a83입니다. 임의로 이 이름을 붙여 컨테이너와 함께 만들어진 레이어를 `container-layer-34a6aa18a83c`라고 이름붙여보겠습니다. 따라서 컨테이너 실행시에 마운트되는 구조는 다음과 같습니다.

```powershell
container-layer-34a6aa18a83c(RW)
nginx-layer3(RO) = nginx:latest
nginx-layer2(RO)
nginx-layer1(RO)
```

`container-layer-34a6aa18a83c` 레이어에는 아무것도 없습니다. 하지만 컨테이너에서 파일 목록을 확인해보면 그 아래 레이어에 있는 내용들이 그대로 보이는 것을 알 수 있습니다. 좀 더 정확히 이야기하자면 nginx-layer1, nginx-layer2, nginx-layer-3, container-layer-34a6aa18a83c의 파일 전체를 마운트한 작업 디렉터리가 하나 있고, 이후에 이 디렉터리에서 일어나는 모든 작업(파일 변경)은 최상위 레이어인 `container-layer-34a6aa18a83c`에 저장됩니다.

다시 한 번 강조하지만, 따라서 그 아래에 있는 레이어들에는 어떠한 변경도 일어나지 않습니다. 아래 레이어에 있었던 파일을 삭제하면 어떻게 될까요? 그걸 처리해주는 게 바로 유니온 마운트의 역할입니다. 이 또한 최상위 레이어에 기록되고, 그 아래에 있는 레이어들에는 어떠한 영향도 주지 않습니다. 따라서 파일을 좀 삭제하고 새로운 컨테이너를 실행하더라도 기존 이미지의 내용이 그대로 남이있습니다.

그럼 도커 데몬을 통해서 실제 컨테이너의 마운트 구조를 확인해보도록하겠습니다.

```powershell
$ docker inspect 34a6aa18a83c | jq '.[].GraphDriver'
{
  "Data": {
    "LowerDir": "/var/lib/docker/overlay2/1f801c214d32d4ccd6e34e4185cca9707fd9b8ec28e2b63b857546e2b53568a1-init/diff:/var/lib/docker/overlay2/10a07b3d72ac36291843eb6ca01698649220065d3b3046f63546fcee49c3c36f/diff:/var/lib/docker/overlay2/7e5bc8d3a02343bf40d479979e734343faff52b8fc768959a24e860c30ae4b74/diff:/var/lib/docker/overlay2/e5b51f307392f7a3776edaa67d5d14b85e04dad9aeca753ac6ad30aaeaa55152/diff",
    "MergedDir": "/var/lib/docker/overlay2/1f801c214d32d4ccd6e34e4185cca9707fd9b8ec28e2b63b857546e2b53568a1/merged",
    "UpperDir": "/var/lib/docker/overlay2/1f801c214d32d4ccd6e34e4185cca9707fd9b8ec28e2b63b857546e2b53568a1/diff",
    "WorkDir": "/var/lib/docker/overlay2/1f801c214d32d4ccd6e34e4185cca9707fd9b8ec28e2b63b857546e2b53568a1/work"
  },
  "Name": "overlay2"
}
```

여기에 컨테이너를 실행할 때 레이어가 마운트되는 모든 정보가 나와있습니다. 이 내용을 이해하기 위해서는 OverlayFS에 대한 이해가 필요합니다. 우선은 `LowerDir`에 이미지 레이어들이 포함되고, `UpperDir`가 컨테이너 레이어가 된다는 정도만 이해하면 됩니다(OverlayFS에 대해서는 뒤에서 조금 더 다룹니다).

컨테이너를 여러개 실행하더라도 이미지 레이어만 공유할 뿐 각각의 컨테이너 전용 쓰기 레이어가 만들어지기 때문에 서로 영향을 주지 않습니다. 컨테이너를 2개 실행하면 다음과 같은 구조가 됩니다.

```powershell
container:34a6aa18a83c
--------------------------------
container-layer-34a6aa18a83c(RW)
nginx-layer3(RO) = nginx:latest
nginx-layer2(RO)
nginx-layer1(RO)


container:47a8bff23fba
--------------------------------
container-layer-47a8bff23fba(RW)
nginx-layer3(RO) = nginx:latest
nginx-layer2(RO)
nginx-layer1(RO)
```

따라서 컨테이너를 아무리 많이 실행시키더라도 실제 쓰기가 이루어지는 레이어가 분리되어있기 때문에 컨테이너들은 서로 영향을 주지 않을 것입니다. 즉, 모든 컨테이너는 고유한 쓰기 영역을 가지며, 이는 최상위 레이어가 되고 하위 레이어에는 어떠한 영향도 주지 않습니다.

여기까지 이해했으면 본격적으로 이미지가 어떻게 만들어지는지 살펴보겠습니다.

## docker diff와 docker commit으로 이미지 만들기

도커 이미지를 직접 만든다고 하면 `Dockerfile`을 떠올리실 겁니다. Dockerfile에는 DSL로 정의된 명령어들로 한 단계씩 도커 이미지 생성 과정을 기술하고, 이를 도커로 실행하면 짠하고 도커 이미지가 만들어집니다. 그런데 도커는 `Dockerfile`로 어떻게 이미지를 생성하는 걸까요?

이를 이해하기 위해서 `docker diff`와 `docker commit` 명령어를 사용해보겠습니다. 실제 업무에서는 거의 사용할 일이 없는 명령어들이니 처음 보시더라도 놀라지 마시기 바랍니다. `docker diff` 명령어부터 알아보겠습니다. 앞서 컨테이너를 실행했을 때 레이어 구성이 어떻게 되는지 살펴보았습니다.

```powershell
container-layer-34a6aa18a83c(RW)
nginx-layer3(RO)
nginx-layer2(RO)
nginx-layer1(RO)
```

컨테이너에서 보이는 파일들은 이 계층들이 모두 합쳐진 모습입니다. 컨테이터는 기본적으로 이미지 계층의 파일들을 기반으로 실행되고, 최상단의 컨테이너 전용 레이어는 처음에는 텅 빈 상태입니다. 그리고 컨테이너에서 일어나는 모든 변경사항들은 최상단 레이어에 기록됩니다. 도커를 처음 배울 때 컨테이너를 종료시키면 변경된 파일들이 날아간다는 얘기를 많이 들어보셨을 겁니다. 그 이유가 여기에 있습니다. 컨테이너에서 일어나는 모든 변경사항은 container-layer-34a6aa18a83c 이 레이어에 저장되고, 컨테이너가 삭제되면 같이 날려버립니다. 즉, 컨테이너 레이어는 기본적으로 휘발적으로 사용됩니다.

`docker diff`는 컨테이너 레이어의 변경사항을 보여주는 명령어입니다. 먼저 컨테이너를 처음 실행했을 때 정말로 아무런 변경사항이 없는지 확인해보겠습니다. 먼저 `nginx:latest` 이미지를 기반으로 `bash`셸 컨테이너를 실행해보겠습니다.

```powershell
$ docker run -it nginx bash
root@238b6c789417:/#
```

다른 창을 하나 더 띄워서 이 컨테이너에 docker diff를 실행해봅니다.

```powershell
$ docker diff 238b6c789417
```

아무것도 출력되지 않으면 정상입니다. 왜냐면 아직 컨테이너 레이어에 아무런 변경사항이 없기 때문입니다. 이 디렉터리를 실제로 확인해보겠습니다. `docker inspect`에서 현재 마운트된 파일 시스템의 `UpperDir`을 확인합니다.

```powershell
$ docker inspect 238b6c789417 | jq '.[].GraphDriver.Data.UpperDir'
/var/lib/docker/overlay2/2d7509079a2bfa110cdfcc26df3232690fa7b970298926a08f47fa22083b6815/diff
```

이 컨테이너에서 일어나는 모든 변경사항은 이 디렉터리에 저장됩니다. 이 디렉터리에 가서 비어있는 것을 확인해봅니다

```powershell
$ pwd
/var/lib/docker/overlay2/2d7509079a2bfa110cdfcc26df3232690fa7b970298926a08f47fa22083b6815/diff
$ ls
```

이제 컨테이너의 bash 셸에서 파일을 하나 만들어봅니다.

```powershell
root@238b6c789417:/# cd tmp
root@238b6c789417:/tmp# touch THIS_IS_CONTAINER
```

다시 `docker diff` 명령어로 변경된 내용을 확인해봅니다.

```powershell
$ docker diff 238b6c789417
C /tmp
A /tmp/THIS_IS_CONTAINER
```

powershell앞의 문자는 변경된 내용을 의미합니다. C는 변경, A는 추가를 의미합니다. 레이어 디렉터리에서도 변경사항을 확인해보겠습니다.

```powershell
$ pwd
/var/lib/docker/overlay2/2d7509079a2bfa110cdfcc26df3232690fa7b970298926a08f47fa22083b6815/diff
$ tree
.
└──tmp
    └──THIS_IS_CONTAINER
```

정확히 컨테이너에서 변경된 내용만이 저장되어있는 것을 확인할 수 있습니다. 이번에는 이미지에 저장되어있는 파일을 하나 삭제해보겠습니다. 컨테이너에서 다음 명령어를 실행합니다.

```powershell
root@238b6c789417:/# rm /bin/tar
root@238b6c789417:/# tar --version
bash: tar: command not found
```

이 파일은 이미지 레이어에 있는 파일입니다. 이렇게 이미지 레이어에 있는 파일을 삭제하더라고 이는 컨테이너 레이어에 기록됩니다. 다시 `diff` 명령어로 변경된 내용을 확인해봅니다.

```powershell
$ docker diff 238b6c789417
C /bin
D /bin/tar
C /tmp
A /tmp/THIS_IS_CONTAINER
```

이번에는 D라는 문자열이 보입니다. 이는 파일이 삭제되었다는 의미입니다. 앞서 이야기했듯이 `docker diff`가 보여주는 것은 컨테이너 레이어의 변경사항이기 때문에 파일 삭제 또한 컨테이너 레이어에 기록되는 것을 확인할 수 있습니다. 실제로 컨테이너 레이어 디렉터리에서는 어떻게 저장되었을까요?

```powershell
$ pwd
/var/lib/docker/overlay2/2d7509079a2bfa110cdfcc26df3232690fa7b970298926a08f47fa22083b6815/diff
$ tree
.
├──bin
│└──tar
└──tmp
    └──THIS_IS_CONTAINER
```

여기는 tar 파일이 추가된 것으로 보여집니다. tree나 ls를 실행시켜보면 색이 살짝 다르게 출력될 것입니다. 이 파일은 일반 파일이 아니라 Character device 형식으로 저장되며, 이는 OverlayFS에서 파일 삭제를 나타내는 특별한 파일입니다. 이 파일은 하위 레이어의 파일이 존재하지 않는 것처럼 가려버리는 역할을 합니다.

다른 컨테이너를 실행시켜서 `nginx:latest` 이미지에서 `tar` 파일이 삭제되지 않은 것을 확인해보겠습니다.

```powershell
$ docker run -it nginx bash
root@46ac6042f551:/# tar --version
tar (GNU tar) 1.30
Copyright (C) 2017 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Written by John Gilmore and Jay Fenlason.
```

즉, 238b6c789417 컨테이너에서의 변경사항은 이미지나 같은 이미지를 사용하는 다른 컨테이너에는 아무런 영향도 끼치지 않습니다.

그럼 이번에는 `docker diff`로 확인 가능한 변경 사항을 이미지로 저장하는 방법을 알아보겠습니다. 바로 이 역할을 수행하는 명령어가 `docker commit`입니다. 바로 사용해보겠습니다. `commit` 명령어는 컨테이너 아이디와 새로운 이미지 이름을 인자 값으로 받습니다.

```powershell
$ docker diff 238b6c789417
C /bin
D /bin/tar
C /tmp
A /tmp/THIS_IS_CONTAINER
$ docker commit 238b6c789417 nginx:without_tar
sha256:f5030dd833b686de064faf55afbc7e45d31b9798f0ebee8d6902edae6b5433ec
$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
nginx               winouth_tar         f5030dd833b6        6 seconds ago       126MB
nginx               latest              231d40e811cd        3 weeks ago         126MB
```

그리고 이 이미지로 컨테이너를 실행하면 tar를 사용할 수 없습니다.

```powershell
$ docker run -it nginx:without_tar bash
root@814638b391a0:/# tar
bash: tar: command not found
root@814638b391a0:/#
```

도커 커밋 명령어는 238b6c789417 컨테이너의 컨테이너용 레이어 container-layer-238b6c789417를 최상단 레이어로 가지는 이미지를 새롭게 생성합니다. 따라서 새롭게 만든 nginx:without_tar 이미지의 레이어 구조는 다음과 같습니다.

```powershell
container-layer-34a6aa18a83c(RO)
nginx-layer3(RO)
nginx-layer2(RO)
nginx-layer1(RO)
```

즉 이 이미지는 4개의 읽기 전용 레이어로 구성되어있습니다. 위의 예제와 같이 `nginx:without_tar` 이미지를 기반으로 컨테이너를 실행하면 이 위에 다시 컨테이너 전용 쓰기 레이어가 추가됩니다. 따라서 다음과 같이 구성됩니다.

```powershell
container-layer-814638b391a0(RW)
container-layer-34a6aa18a83c(RO)
nginx-layer3(RO)
nginx-layer2(RO)
nginx-layer1(RO)
```

그렇다면 `docker history` 명령어로 레이어를 확인해보겠습니다.

```powershell
$ docker history nginx:without_tar
IMAGE               CREATED             CREATED BY                                      SIZE                COMMENT
2866e7228b7a        2 minutes ago       bash                                            0B
231d40e811cd        3 weeks ago         /bin/sh -c #(nop)  CMD ["nginx" "-g" "daemon.   0B
<missing>           3 weeks ago         /bin/sh -c #(nop)  STOPSIGNAL SIGTERM           0B
<missing>           3 weeks ago         /bin/sh -c #(nop)  EXPOSE 80                    0B
```

231d40e811cd는 nginx:latest 이미지입니다. 그 위에 `bash` 명령어로 만든 2866e7228b7a 이미지가 있는 것을 확인할 수 있습니다. 이 이미지가 바로 방금 전에 생성한 `nginx:without_tar` 이미지입니다. 여기서 `bash`라고 나오는 것은 처음에 컨테이너를 bash로 실행했기 때문입니다.

이게 바로 도커 이미지가 만들어지는 기본적인 원리입니다. 컨테이너를 만들고, 새로운 레이어에 변경사항을 더하고, 이 내용을 커밋해서 읽기 전용 레이어로 기존 이미지에 쌓아올려서 새로운 이미지를 만듭니다.

## 도커 커밋으로 이미지 만들기, Dockerfile로 이미지 만들기

앞서 `docker commit` 명령어를 사용해서 컨테이너에서 직접 이미지를 만들어보았습니다. 컨테이너와 이미지는 마치 별개인 것처럼 느껴지지만, 이미지가 실제로는 컨테이너를 기반으로 만들어진다는 사실을 꼭 기억해야합니다. 앞에서는 이해를 위해 파일을 추가하거나 삭제하는 의미없는 작업을 했습니다만, 이번에는 좀 더 실용적인 예제로 도커 빌드의 원리에 대해서 알아보고자합니다.

이번에 만들 이미지는 깃Git이 설치된 우분투Ubuntu 이미지입니다. Dockerfile을 사용할 수도 있습니다만, 이해를 돕기 위해 앞서 배운 `docker commit` 명령어로 한 단계씩 이미지를 만들어보겠습니다. 먼저 우툰부 이미지에 git이 없는 것부터 확인해봅니다.

```powershell
$ docker pull ubuntu:focal
$ docker run -it ubuntu:focal /bin/sh -c 'git --version'
/bin/sh: 1: git: not found
```

이제 이 이미지에 git을 설치해보겠습니다.

```powershell
$ docker run ubuntu:focal /bin/sh -c 'apt-get update' 
$ docker commit $(docker ps -alq) ubuntu:git-layer-1

$ docker run ubuntu:git-layer-1 /bin/sh -c 'apt-get install -y git'
$ docker commit $(docker ps -alq) ubuntu:git
```

여기서는 두 단계에 걸쳐서 git을 설치했습니다. 먼저 `apt-get update` 명령어를 실행한 다음 이 레이어를 `ubuntu:git-layer-1`(중간 레이어) 이미지로 저장했습니다. 여기서 `$(docker ps -alq)`는 가장 최근에 만들어진 컨테이너 ID로 치환됩니다.

두 번째로 `ubuntu:git-layer-1` 이미지에서 `apt-get install -y git` 명령어로 git을 설치했습니다. 그리고 이 레이어를 `ubuntu:git` 이미지로 저장했습니다. 이 이미지에 `git`이 잘 설치되었는지 확인해보겠습니다.

```powershell
$ docker run -it ubuntu:git bash -c 'git --version'
git version 2.24.0
```

정상적으로 `git` 명령어가 동작하는 것을 확인할 수 있습니다. 이번에는 `docker history`로 이미지의 계층을 살펴보겠습니다.

```powershell
$ docker history ubuntu:git
IMAGE               CREATED             CREATED BY                                      SIZE                COMMENT
6e5927f3f9ed        9 minutes ago       /bin/sh -c apt-get install -y git                          108MB
2bd69eb491fc        11 minutes ago      /bin/sh -c apt-get update                                  21.1MB
cea566af5cae        6 weeks ago         /bin/sh -c #(nop)  CMD ["/bin/bash"]            0B
<missing>           6 weeks ago         /bin/sh -c mkdir -p /run/systemd && echo 'do.   7B
<missing>           6 weeks ago         /bin/sh -c set -xe   && echo '#!/bin/sh' > /.   811B
<missing>           6 weeks ago         /bin/sh -c [ -z "$(apt-get indextargets)" ]     985kB
<missing>           6 weeks ago         /bin/sh -c #(nop) ADD file:6d50e196f48c898ea.   72.2MB
```

이미지 ID가 된 부분은 `ubuntu:focal` 이미지를 만들면서 생성된 레이어입니다. `cea566af5cae`는 `ubuntu:focal` 이미지의 레이어입니다. 그 위로는 방금 생성한 레이어들이 쌓여있는 것을 확인할 수 있습니다. 이미지를 만들 때 사용한 컨테이너에서 실행한 명령어도 정확히 기록된 것을 확인할 수 있습니다. 그리고 각 레이어에서 추가된 용량도 나타납니다. 새로운 레이어들의 용량은 129.1MB이 됩니다. 이는 `docker images`에서도 확인할 수 있습니다.

```powershell
$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
ubuntu              git                 6e5927f3f9ed        11 minutes ago      202MB
ubuntu              focal               cea566af5cae        6 weeks ago         73.2MB
```

`ubuntu:focal`과 `ubuntu:git` 이미지의 용량 차이가 약 129메가인 것을 확인할 수 있습니다.

그럼 이번에는 Dockerfile로 같은 이미지를 만들어보겠습니다. 위 내용을 Dockerfile로 바꾸는 것은 어렵지 않습니다.

```powershell
FROM ubuntu:focal
RUN apt-get update
RUN apt-get install -y git
```

앞서 작업했던 것과 거의 똑같죠? 이 내용을 `Dockerfile`로 저장하고 `build` 명령어로 `ubuntu:git2`라는 이름의 이미지를 만들어봅니다.

```powershell
$ docker build -t ubuntu:git2 .
Sending build context to Docker daemon  2.048kB
Step 1/3 : FROM ubuntu:focal
 ---> cea566af5cae
Step 2/3 : RUN apt-get update
 ---> Running in a349c7070216
...
Removing intermediate container a349c7070216
 ---> 3836c7981d11
Step 3/3 : RUN apt-get install -y git
 ---> Running in 8f4bf61fbe0d
...
Removing intermediate container 8f4bf61fbe0d
 ---> 3c38db3252b8
Successfully built 3c38db3252b8
Successfully tagged ubuntu:git2
```

출력되는 내용이 상당히 많습니다. 여기서는 도커 빌드 과정에서 실행되는 명령어의 출력 결과는 제외하고, `docker build` 명령어 자체의 출력 결과만 남겨보았습니다.

먼저 `Step 1/3`은 `FROM ubuntu:focal`을 실행하는 단계입니다. `FROM`은 새로 생성하는 이미지의 베이스 이미지를 지정하는 명령어입니다. 다음 줄에 있는 `cea566af5cae` 다이제스트 값은 `ubuntu:focal`의 이미지 ID입니다.

그 다음 단계는 `Step 2/3 : RUN apt-get update`입니다. 다음 세 줄에 주목해주시기 바랍니다.

```powershell
 ---> Running in a349c7070216
...
Removing intermediate container a349c7070216
 ---> 3836c7981d11
```

무언가를 실행하고, 그 다음에 정확히 같은 다이제스트 값을 지우는데 컨테이너를 지웠다고 나와있습니다. 이 사이에서 일어난 일을 이해하는 것이 중요합니다. Dockerfile의 RUN은 단순히 셸 명령어를 실행하는 작업이 아닙니다. 바로 전 스텝의 이미지(cea566af5cae)를 기반으로 컨테이너를 실행하고(a349c7070216) RUN에 지정된 명령어를 실행합니다. 그리고 이 컨테이너를 커밋해서 새로운 이미지(3836c7981d11)로 저장합니다. 마지막 줄에 다이제스트 값이 바로 중간 이미지의 ID값입니다. 친절하지는 않지만, 이러한 과정이 충실히 기록되어있습니다.

RUN 명령어가 하나 더 있으니 똑같은 과정을 한 번 더 거칩니다. 이번에는 `git`을 설치합니다.

```powershell
Step 3/3 : RUN apt-get install -y git
 ---> Running in 8f4bf61fbe0d
...
Removing intermediate container 8f4bf61fbe0d
 ---> 3c38db3252b8
Successfully built 3c38db3252b8
Successfully tagged ubuntu:git2
```

이번에 만들어진 이미지 아이디는 3c38db3252b8입니다. 그리고 이 이미지에 `ubuntu:git2`라는 이름을 태그해줍니다. git이 정상적으로 설치되었는지 한 번 확인해보겠습니다.

```powershell
$ docker run -it ubuntu:git2 bash -c 'git --version'
git version 2.24.0
```

이번에도 정상 동작하네요. `docker history`로 이미지 레이어들을 확인해보겠습니다.

```powershell
$ docker history ubuntu:git2
IMAGE               CREATED              CREATED BY                                      SIZE                COMMENT
3c38db3252b8        About a minute ago   /bin/sh -c apt-get install -y git               108MB
3836c7981d11        About a minute ago   /bin/sh -c apt-get update                       21.1MB
cea566af5cae        6 weeks ago          /bin/sh -c #(nop)  CMD ["/bin/bash"]            0B
<missing>           6 weeks ago          /bin/sh -c mkdir -p /run/systemd && echo 'do.   7B
<missing>           6 weeks ago          /bin/sh -c set -xe   && echo '#!/bin/sh' > /.   811B
<missing>           6 weeks ago          /bin/sh -c [ -z "$(apt-get indextargets)" ]     985kB
<missing>           6 weeks ago          /bin/sh -c #(nop) ADD file:6d50e196f48c898ea.   72.2MB
```

이미지 ID가 다른 것을 빼면 `ubuntu:git`와 `ubuntu:git2`의 `history`와 거의 같은 것을 확인할 수 있습니다.

실제 애플리케이션을 도커라이즈할 때는 훨씬 더 긴 Dockerfile을 작성하게 됩니디만, 이미지가 생성되는 기본적인 원리는 동일합니다. 베이스 이미지에서 컨테이너로 명령어를 실행하고, 여기서 변경된 내용을 이미지로 저장합니다. 그리고 이 이미지를 기반으로 다시 컨테이너로 명령어를 실행하고, 다시 변경된 내용을 이미지로 저장합니다. 이 과정을 Dockerfile이 끝날 때까지 반복합니다. 즉, Dockerfile 한줄 한줄이 컨테이너로 실행되고 이미지로 만들어집니다.

재미있는 포인트는 이렇게 직접 도커 데몬에서 빌드한 이미지는 중간 이미지가 전부 남는다는 점입니다. 이는 커밋을 직접한 경우나 도커 빌드를 한 경우 둘 다 마찬가지입니다. 생각해보면 당연한 일입니다. 예를 들어 `apt-get update`만 실행한 이미지에서 컨테이너를 실행하는 게 가능합니다. 이 중간 이미지에서 `git`이 실행가능한지 간단하게 테스트해보겠습니다.

```powershell
# docker commit으로 명시적으로 생성한 중간 이미지의 경우
$ docker run -it ubuntu:git-layer-1 /bin/sh -c 'git --verison'
/bin/sh: 1: git: not found

# docker build 중에 생성된 중간 이미지의 경우
$ docker run -it 3836c7981d11 /bin/sh -c 'git --version'
/bin/sh: 1: git: not found
```

예상하셨겠지만 두 경우 모두 `git`이 실행되지 않습니다. 도커 빌드를 한 경우 `docker image -a`를 실행하면 이름 없는 이미지들이 출력되는데, 이것들이 이미지 빌드 과정에서 생성된 이미지들입니다. 도커의 빌드 원리를 이해한다면, 도커 빌드 중에 에러가 발생했을 때 중간 이미지에서 셸을 실행해서 어떤 문제가 있는지 직접 확인하는 작업도 가능합니다.

## 이미지 직접 빌드하고 중간 레이어에서 컨테이너 실행하기

앞서 살펴봤듯이 이미지를 풀 받는 대신 직접 빌드하면 중간 레이어가 모두 이미지로 남습니다. 따라서 최종 이미지가 아닌 중간 이미지에 접근하기 위한 가장 확실한 방법은 이미지를 로컬에서 직접 빌드하는 방법입니다.*****

***** 단, 빌드 시점이나 환경의 차이로 인해서 풀 받은 이미지와 직접 빌드한 이미지가 완전히 같다는 것을 보장할 수는 없습니다.

다시 한 번 `nginx` 이미지의 `history`를 확인해보겠습니다.

```powershell
$ docker history nginx:latest
IMAGE               CREATED             CREATED BY                                      SIZE                COMMENT
231d40e811cd        3 weeks ago         /bin/sh -c #(nop)  CMD ["nginx" "-g" "daemon.   0B
<missing>           3 weeks ago         /bin/sh -c #(nop)  STOPSIGNAL SIGTERM           0B
<missing>           3 weeks ago         /bin/sh -c #(nop)  EXPOSE 80                    0B
<missing>           3 weeks ago         /bin/sh -c ln -sf /dev/stdout /var/log/nginx.   22B
<missing>           3 weeks ago         /bin/sh -c set -x     && addgroup --system -.   57.1MB
<missing>           3 weeks ago         /bin/sh -c #(nop)  ENV PKG_RELEASE=1~buster     0B
<missing>           3 weeks ago         /bin/sh -c #(nop)  ENV NJS_VERSION=0.3.7        0B
<missing>           3 weeks ago         /bin/sh -c #(nop)  ENV NGINX_VERSION=1.17.6     0B
<missing>           3 weeks ago         /bin/sh -c #(nop)  LABEL maintainer=NGINX Do.   0B
<missing>           3 weeks ago         /bin/sh -c #(nop)  CMD ["bash"]                 0B
<missing>           3 weeks ago         /bin/sh -c #(nop) ADD file:bc8179c87c8dbb3d9.   69.2MB
```

`nginx` 공식 이미지의 Dockerfile은 다음 저장소에서 관리되고 있습니다.

- https://github.com/nginxinc/docker-nginx/

여기서 Dockerfile을 다운로드 받아 직접 빌드해보겠습니다.

```powershell
$ mkdir nginx
$ cd nginx 
$ https://raw.githubusercontent.com/nginxinc/docker-nginx/master/mainline/buster/Dockerfile
$ docker build -t 44bits/nginx .
```

새로 만든 이미지에 대해서 history를 출력해봅니다.

```powershell
$ docker history 44bits/nginx
IMAGE               CREATED              CREATED BY                                      SIZE                COMMENT
7c510ed44632        17 seconds ago       /bin/sh -c #(nop)  CMD ["nginx" "-g" "daemon.   0B
0c861df9b6da        18 seconds ago       /bin/sh -c #(nop)  STOPSIGNAL SIGTERM           0B
52dc89e66f0c        18 seconds ago       /bin/sh -c #(nop)  EXPOSE 80                    0B
03dcdc90b6e6        18 seconds ago       /bin/sh -c ln -sf /dev/stdout /var/log/nginx.   22B
2452c200da29        20 seconds ago       /bin/sh -c set -x     && addgroup --system -.   57.1MB
709c003164a5        About a minute ago   /bin/sh -c #(nop)  ENV PKG_RELEASE=1~buster     0B
6e31e301a253        About a minute ago   /bin/sh -c #(nop)  ENV NJS_VERSION=0.3.7        0B
ebb022c8fa37        About a minute ago   /bin/sh -c #(nop)  ENV NGINX_VERSION=1.17.6     0B
e705fa94c0bb        7 hours ago          /bin/sh -c #(nop)  LABEL maintainer=NGINX Do.   0B
2dbffcb4f093        3 weeks ago          /bin/sh -c #(nop)  CMD ["bash"]                 0B
<missing>           3 weeks ago          /bin/sh -c #(nop) ADD file:bc8179c87c8dbb3d9.   69.2MB
```

중간 이미지들의 ID들이 출력되는 것을 확인할 수 있습니다! 도커 컨테이너를 실행할때 이 이미지들의 아이디를 지정하면, 중간 이미지에서 도커 컨테이너를 실행해보는 것이 가능합니다.

## OverlayFS 직접 사용해보고, 임의의 위치에 도커 이미지 마운트하기

도커 이미지를 제대로 이해하려면 결국 OverayFS 혹은 유니온 마운트 개념을 이해할 필요가 있습니다. 유니온 마운트가 오늘의 메인 주제는 아닙니다만, 이야기가 나온 김에 조금만 더 자세히 알아보겠습니다.

OverlayFS를 사용하는 아주 간단한 예를 살펴보고, 직접 위의 컨테이너와 같은 파일 시스템을 구축해보겠습니다.

```powershell
$ mkdir overlayfs; cd overlayfs
$ mkdir container image1 image2 merge work
$ touch image1/a image1/b image2/c
$ sudo mount -t overlay overlay -o lowerdir=image2:image1,upperdir=container,workdir=work merge
```

먼저 5개의 디렉터리를 만들었습니다. `work`는 직접 사용하지 않으므로, `work` 디렉터리가 필요하다는 정도만 기억해두시면 됩니다. 실제로 데이터가 들어가는 디렉터리는 `contanier`와 `image1`, `image2`입니다. 구성하고자 하는 디렉터리(레이어) 계층은 다음과 같습니다.

```
container(최상위) = upperdir
image2
image1
```

`container`는 최상위 디렉터리가 됩니다. OverlayFS에서 최상위 디렉터리는 `upperdir`로 나타냅니다. 나머지 하위 데이터 디렉터리는 모두 `lowerdir`에 포함됩니다. `lowerdir`은 `:`로 구분되며 맨 뒤에서부터 앞으로 쌓아나갑니다. 따라서 위와 같은 구조는 다음과 같이 표현됨니다: `lowerdir=image2:image1`. `merge` 디렉터리는 모든 계층을 쌓여서(겹쳐서) 보여지는 디렉터리입니다. 실제 작업은 이 merge 디렉터리에서 이루어지고, 변경사항은 `upperdir`에 저장됩니다. 이와 같은 내용을 참고해서 mount 명령을 실행하면 준비는 끝이 납니다.

이제 실제로 잘 적용이 되었는지 확인해보겠습니다.

```powershell
$ tree . -I work
.
├──container
├──image1
│├──a
│└──b
├──image2
│└──c
└──merge
    ├──a
    ├──b
    └──c
```

이미지들의 파일들이 merge 디렉터리에 합쳐서 보여지는 것을 알 수 있습니다. 컨테이너와 마찬가지로 최상위 레이어인 container는 비어있습니다. merge 디렉터리에 파일을 변경하면, 모든 변경사항은 upperdir인 container 디렉터리에 저장됩니다. merge 디렉터리에서 a 파일을 삭제하고 d 파일을 추가해보겠습니다.

```powershell
$ rm ./merge/a
$ touch ./merge/d
$ tree . -I work
.
├──container
│├──a
│└──d
├──image1
│├──a
│└──b
├──image2
│└──c
└──merge
    ├──b
    ├──c
    └──d
```

변경이 일어나기 전과 비교해보시기 바랍니다. `merge` 디렉터리에서는 정확히 우리가 의도한 대로 `a`가 삭제되었고, `d`가 추가되었습니다. 그리고 우선 `container` 디렉터리에 `d` 파일이 추가된 것을 확인할 수 있습니다. 그리고 재미있게도 `container` 디렉터리에 `a`라는 파일도 추가되어있네요. 이는 앞에서 잠깐 설명했었는데 Character device라는 특수한 형식의 파일로 삭제된 파일을 의미합니다. 그리고 `image1`과 `image2`에는 아무런 변화도 없습니다.OverlayFS의 동작 방식이 대충 감이 오시나요? 직접 파일을 추가하거나 삭제해보면서 실험해보는 걸 추천드립니다.

자, 이제 도커 이야기로 넘어가겠습니다. 도커는 내부적으로 OverlayFS를 똑같이 사용합니다. 앞서 예제를 다루던 중에 도커 컨테이너의 속성 중에서 GraphDriver를 확인했던 게 기억나시나요?

```powershell
$ docker inspect 34a6aa18a83c | jq '.[].GraphDriver'
{
  "Data": {
    "LowerDir": "/var/lib/docker/overlay2/1f801c214d32d4ccd6e34e4185cca9707fd9b8ec28e2b63b857546e2b53568a1-init/diff:/var/lib/docker/overlay2/10a07b3d72ac36291843eb6ca01698649220065d3b3046f63546fcee49c3c36f/diff:/var/lib/docker/overlay2/7e5bc8d3a02343bf40d479979e734343faff52b8fc768959a24e860c30ae4b74/diff:/var/lib/docker/overlay2/e5b51f307392f7a3776edaa67d5d14b85e04dad9aeca753ac6ad30aaeaa55152/diff",
    "MergedDir": "/var/lib/docker/overlay2/1f801c214d32d4ccd6e34e4185cca9707fd9b8ec28e2b63b857546e2b53568a1/merged",
    "UpperDir": "/var/lib/docker/overlay2/1f801c214d32d4ccd6e34e4185cca9707fd9b8ec28e2b63b857546e2b53568a1/diff",
    "WorkDir": "/var/lib/docker/overlay2/1f801c214d32d4ccd6e34e4185cca9707fd9b8ec28e2b63b857546e2b53568a1/work"
  },
  "Name": "overlay2"
}
```

이 내용을 바탕으로 직접 도커 컨테이너의 작업 디렉터리를 구성해보는 게 가능합니다. OverlayFS를 마운트하기 위한 필요한 모든 정보를 여기서 찾을 수 있습니다.

```powershell
$ mkdir container-overlayfs; cd container-overlayfs
$ mkdir container merge work
$ sudo mount -t overlay overlay -o upperdir=container,workdir=work,lowerdir=/var/lib/docker/overlay2/1f801c214d32d4ccd6e34e4185cca9707fd9b8ec28e2b63b857546e2b53568a1-init/diff:/var/lib/docker/overlay2/10a07b3d72ac36291843eb6ca01698649220065d3b3046f63546fcee49c3c36f/diff:/var/lib/docker/overlay2/7e5bc8d3a02343bf40d479979e734343faff52b8fc768959a24e860c30ae4b74/diff:/var/lib/docker/overlay2/e5b51f307392f7a3776edaa67d5d14b85e04dad9aeca753ac6ad30aaeaa55152/diff merge
```

`container`, `work`, `merge`는 직접 만든 디렉터리를 사용했습니다. 바꿔줄 부분은 lowerdir입니다. `docker inspect`에 출력된 `lowerdir` 정보를 그대로 복사해 넣어주시면 됩니다.

```powershell
$ ls merge/
bin  boot  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
```

짠, nginx 도커 이미지에 컨테이너 레이어를 더해서 마운트하는데 성공했습니다. 물론 이는 이미지를 특정 디렉터리에 마운트 시킨 것 뿐이기 때문에 컨테이너는 아닙니다. 프로세스의 루트 디렉터리를 격리시켜주는 chroot를 사용하면 컨테이너 흉내를 내보는 것도 가능합니다.

```powershell
$ sudo chroot ./merge nginx -g 'daemon off;'
```

다른 창에서 `0.0.0.0:80`에 curl로 접근해보면 정상적으로 결과가 출력되는 것을 확인할 수 있습니다. 그리고 여기서 발생하는 모든 내용은 위에서 만든 `container` 디렉터리에 저장됩니다.
