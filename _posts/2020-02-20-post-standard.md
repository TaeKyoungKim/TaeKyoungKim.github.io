## GitHub에 사이트 만들기(나만의 방법)

#### 1. 시도 

여러가지 시도를 해보았다. google에 있는 방법들을 그대로 따라 했는데 잘 안되는 부분이 있었다 .. 내 실력이 부족해서 그런지 막히는 부분들이 있어 다양한 설명들을 조합하면 어떨까 하는 생각이 들어서 조합의 형태로 시도함

가장 맘에드는 테마를 찾아서 사용하는 방법을 택함

#### 2. 방법 

##### 1) 먼저 [jekyll](https://jekyllrb.com/) 사이트 방문 

​	

```powershell
  gem install bundler jekyll

  jekyll new my-awesome-site

  cd my-awesome-site

  bundle exec jekyll serve

# => Now browse to http://localhost:4000
```

등의 기초 명령어를 이용해 직접 만들어 볼수 도 있다. 

자세한 것은 사이트를 들어 가서 보면 될듯 

사이트의 메뉴중에 [Resources](https://jekyllrb.com/resources/) 메뉴를 클릭에서 여러가지 살펴 보다가 한가지를 

택함(물론 그 전에 많은 설명사이트를 거치면서 시행 착오를 거치고 나만에 방법을 찾아서)

[블로그 테마](https://jekyllthemes.io/jekyll-blog-themes)도 구경하면서 여러가지 살편 보다가 구글링을 내가 찾는건 so-simple-theme라

구글링을 통해 [so-simple-theme](https://github.com/mmistakes/so-simple-theme) 에 들어가서 다운로드 받음



##### 2) 나의 로컬에서 테스트

```powershell
git clone https://github.com/mmistakes/so-simple-theme
```

나는 apps라는 폴더를 만들어 사용하여서 아래  폴더에 들어감

```
cd so-simple-theme
```



example 에 있는 사이트를 사용해 보기 위해 폴더로 들어간후

```shell
cd example
bundle install 
bundle exec jekyll serve
```

다음과 같은 과정을 거치면 

http://localhost:4000/example/ 사이트를 확인 할 수 있다.

<img width="1434" alt="스크린샷 2020-02-20 오후 8 29 54" src="https://user-images.githubusercontent.com/25717861/74933215-e2df5900-5426-11ea-9f04-c7ca2b95d834.png" style="zoom:50%;">



posts 메뉴를 클릭 했을때의 모습

<img src=https://user-images.githubusercontent.com/25717861/74933472-5bdeb080-5427-11ea-816b-f8caae0e0c77.png" alt="image-20200220203108650" style="zoom:50%;" />

이 부분에서 posts폴더 부분의 파일 명을 보면서 변화를 관찰해 보면 

2009-05-15-edge-case-nested-and-mixed-lists.md

2018-02-25-hidden-post.md

2010-10-25-post-future-date.md 등을 살표보면 각각이 " -" 를 기준으로 어떤부분에 어떻게 분류되어 나타나는지 알 수 있다

이부분에 대한건 다음에 한번 포스팅 해봐야 겠다.

예를 들어 

2010-10-25-post-future-date.md

파일의 내용에서 

---

title: "Post: Future Date"
date: 2021-12-31
categories:

  - Post
    last_modified_at: 2017-03-09T12:45:25-05:00

---

This post lives in the future and is dated {{ page.date | date: "%c" }}. It should only appear when Jekyll builds your project with the `--future` flag.

```bash
jekyll build --future
```

date: 2021-12-31 에 의해서 그 시점에 포스트가 올라가게 되어 있다.



이제 로컬에서 확인 한것을 나의 사이트로 써먹기 위해서 나이 [github](https;//github.com) 에서 새로운 프로젝트 생성한다. 



<img width="768" alt="스크린샷 2020-02-20 오후 9 25 54" src="https://user-images.githubusercontent.com/25717861/74933572-a2340f80-5427-11ea-8e54-148d84f61fb1.png">


이미 만들어져 있어 경고 창이 나오지만 만들어져 있지 않으면 경고창이 안뜬다.

여기서 체크 하고 넘어가야 하는 부분은 깃허브의 본인의 username과 같은 이름으로 만들면

http://taekyoungkim.gthub.io 로 접속해서 사용 할 수 있지만 그렇지 않고 이름을 달리 했다면 http://taekyoungkim.gthub.io /<특정이름> 이렇게 들어가야 하는 불편함이 있으므로 목적에 맞게 사용하면 될듯 하다.

Create repository를 누루고 생성하면 되는데 README.md파일을 생성을 체크 하라고 나대부분에 설명은 나오는데 굳이 체크 할 필요 없다는게 나이 결론이다.

원격 Repository가 생성되었다면 

다음은 로컬에 다운받아 테스트 해본 so-simple-theme의 example 폴더안에 내용을 복사에서 활용한다.

```powershell
mkdir mybookblog 
cd mybookblog
```



형식으로 만든후 so-simple-theme의 example의 내용을 복사해서 붙히기 한다.

<img width="305" alt="스크린샷 2020-02-20 오후 9 27 30" src="https://user-images.githubusercontent.com/25717861/74933710-ee7f4f80-5427-11ea-9dad-4fde27d55ee0.png" style="zoom:50%">

위의 내용은 example 폴더에 있는 것을 복사해 왔다 하지마 이부분에서 주목해야 하는 것은

<img src="https://user-images.githubusercontent.com/25717861/74933755-08209700-5428-11ea-8b41-80d40c031d44.png" alt="image-20200220205018411" style="zoom:50%;" />

비교 했을때 첨가된 폴더와 파일이다.

_includes , _layouts, _sass 폴더와 jekyll-theme-so-simple.gemspec 파일이다.

이부분을 so-simple-theme에서 복사해서 붙혀 넣어주면 된다.

마지막으로 중요한 부분이 

Germile을 열고 다음과 같이 

```
gem "jekyll-theme-so-simple", path: "./"
```

path 부분을 지금 폴더를 기본 경로로 하게 위와 같이 지정해 준다.



다음 

_config.yml을 각자의 취향에 맡게 작성하여 주면 된다.

잠깐!

url: "https://TaeKyoungKim.github.io" 이부분은 꼭 수정해야 되는 부분? 이다.

_config.yml 이부분의 자세한 내용은 다음 포스트에서 정리하여 본다.
