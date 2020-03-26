# go lang 이란?

#### 1.Go 개발자들

GO 프로그래밍 언어는 2007년 구글에서 개발을 시작하여 2012년 GO 버젼 1.0을 완성하였다. GO는 이후 계속 향상된 버젼을 내 놓았으며 2015년 말에는 1.5.2 버젼에 이르렀다.

흔히 golang 이라고도 불리우는 Go 프로그래밍 언어는 구글의 V8 Javascript 엔진 개발에 참여했던 Robert Griesemer, Bell Labs에서 유닉스 개발에 참여했던 Rob Pike, 
그리고 역시 Bell Labs에서 유닉스 개발했으며 C 언어의 전신인 B 언어를 개발했던 Ken Thompson이 함께 개발하였다.

#### 2. Go 프로그래밍 언어의 특성

Go는 전통적인 컴파일, 링크 모델을 따르는 범용 프로그래밍 언어이다. Go는 일차적으로 시스템 프로그래밍을 위해 개발되었으며, C++, Java, Python의 장점들을 뽑아 만들어졌다. C++와 같이 Go는 컴파일러를 통해 컴파일되며, 정적 타입 (Statically Typed)의 언어이다. 
또한 Java와 같이 Go는 Garbage Collection 기능을 제공한다. Go는 단순하고 간결한 프로그래밍 언어를 지향하였는데, Java의 절반에 해당하는 25개의 키워드만으로 프로그래밍이 가능하게 하였다. 마지막으로 Go의 큰 특징으로 Go는 Communicating Sequential Processes (CSP) 스타일의 Concurrent 프로그래밍을 지원한다



#### 3. 설치

Go 프로그래밍을 시작하기 위해 Go 공식 웹사이트인 http://golang.org/dl 에서 해당 OS 버젼의 Go를 다운로드하여 설치한다. Go는 Windows, Linux, Mac OS X 에서 사용할 수 있다.

윈도우즈에 Go를 설치하기 위해서는 MSI (*.msi) 파일을 다운받아 실행하면 되는데, Go는 디폴트로 C:\go 폴더에 설치되며, MSI가 C:\go\bin을 PATH 환경변수를 추가한다. (*주: 여기서는 별도의 언급이 없는 한 Windows에 설치된 Go를 기준으로 설명*)

리눅스에서 Go를 사용하기 위해서는 [[팁 - 리눅스에서 Go 설치하기\]](http://golang.site/go/article/201-리눅스에-Go-설치하기)를, Mac OS X에서 Go를 사용하기 위해서는 [[팁 - Mac에서 Go 설치하기\]](http://golang.site/go/article/202-Mac에-Go-설치하기) 링크를 참조한다.



#### 4.GO 실행 및 테스트

Go가 설치되었으면, Go를 간단하게 실행해보는 테스트를 해 볼 수 있다. Go가 디폴트인 C:\Go 폴더에 설치되었다 가정하고 NotePad로 아래 코드를 작성하여 C:\Go\bin\test.go 파일로 저장해 보자. 
(*주: 실제로는 별도의 Go 작업폴더(Workspace)를 만들어서 그곳에 소스를 생성한다. 여기서는 아주 간단한 테스트이므로 작업폴더 없이 Go를 실행해 본다.*)

```go
package main
func main() {
    println("Test")
}
```

다음 bin 디렉토리로 이동한 후 다음과 같이 go 프로그램을 실행할 수 있다. Go는 run 명령어를 사용하면 직접 컴파일과 동시에 실행하게 된다. 
이때 실행파일 .exe 는 만들어지지 않는다.

```shell
C:\Go\bin> go run test.go
```

실행파일 .exe 을 생성하기 위해서는 다음과 같이 go build 명령을 사용한다.

```shell
C:\Go\bin> go build test.go
```



#### 5.Workspace 폴더

Go 프로그래밍을 위해 일반적으로 Workspace 폴더 (작업 폴더)를 생성하는데, 이 폴더 안에는 3개의 서브디렉토리 (bin, pkg, src)를 생성한다. 
예를 들어, C:\GoApp 디렉토리를 Workspace 폴더로 정했다면, C:\GoApp 안에 bin, pkg, src 서브 폴더를 만들어 준다.

Workspace 폴더를 생성한 후, GOPATH 환경변수에 이 Workspace 폴더 경로를 추가해 준다 (SET GOPATH=C:\GoApp 처럼 세션별로 할 수 있으나, 
주로 시스템 설정에서 시스템 환경변수 혹은 사용자 환경변수로 지정한다).
GOPATH는 하나 이상의 경로를 지정할 수 있다. 즉, 여러 Workspace가 있는 경우, 이들 경로를 계속 추가할 수 있다.

Go는 2개의 중요한 환경변수(GOROOT와 GOPATH)를 사용한다.
*GOROOT*: Go가 설치된 디렉토리(윈도우즈의 경우 디폴트로 C:\Go)를 가리키며, Go 실행파일은 GOROOT/bin 폴더에, Go 표준 패키지들은 GOROOT/pkg 폴더에 있다. 
(윈도우즈에 GO 설치시 시스템 환경변수로 자동으로 설정된다)
*GOPATH*: Go는 표준 패키지 이외의 3rd Party 패키지나 사용자 정의 패키지들을 이 GOPATH 에서 찾는다. 복수 개의 경로를 지정한 경우, 3rd Party 패키지는 처음 경로에 설치된다.

Go 환경변수는 go env 를 실행하여 체크할 수 있다.

![go-env](http://golang.site/images/basics/go-env.png)



#### 6.편리한 Go편집기 vscode 설치하기



#### 7. Web-Based Go 편집 및 테스트

http://play.golang.org 웹사이트를 사용하면, 웹에서 Go 프로그램을 편집하고 직접 실행, 
테스트해 볼 수 있다. Intellisense 기능이 제공되지 않는 단점이 있지만, 간단한 프로그램 테스트 혹은 스터디 용으로 사용될 수 있다.
