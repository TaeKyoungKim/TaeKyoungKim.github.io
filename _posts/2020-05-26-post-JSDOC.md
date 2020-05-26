### JSDoc란

**Javasript 소스코드 파일에 주석을 달기위해 사용되는 마크업언어**입니다.

JSDoc에 포함하는 주석을 사용하여 코드를 작성하고 인터페이스를 설명하는 문서를 생성할 수 있습니다.



![img](https://k.kakaocdn.net/dn/chk4qm/btqCEOip81A/upaZ2k0i7WGMawjK2pp8eK/img.png)전체 이미지 / docdash 템플릿



 

#### JSDoc 설치 / 사용법

\0. 프로젝트 설정

JSDoc을 설정하려는 프로젝트 폴더에서 진행한다.

```
// cmd
npm init -y
```

 

\1. 설치

```
// cmd
npm i --save-dev jsdoc
```

테마 설치

https://github.com/clenemt/docdash

```
// cmd
npm install docdash
```

 

\2. 해당하는 파일 문서화(jsdoc.conf 사용 시 파일에 작성된 incloude에 적힌 경로로 적용됨)

\- 단일 파일



![img](https://k.kakaocdn.net/dn/UGdM4/btqCBxaOFGV/TqIgYjH6lOPIAriWx9W9ZK/img.png)단일 파일



```
// cmd
jsdoc index.js
```

 

\- 단일 폴더내에 복수 파일



![img](https://k.kakaocdn.net/dn/L7KpG/btqCBwJKYTs/FDFKtY8nToKS1FiK7LNbjk/img.png)단일 폴더내에 복수파일



```
// cmd
jsdoc ./js
```

 

\- 복수 파일



![img](https://k.kakaocdn.net/dn/AAOxE/btqCB7JST8a/hu7ZBmXwWx4UFf3CzJyrE0/img.png)복수 파일



```
//cmd
jsdoc ./js main.js
```

 

\3. jsdoc.conf 설정하기

루트 폴더의 위치에서 jsdoc.conf 파일 생성 후 아래 코드 삽입

\1. include의 경로 수정할 것 (해당파일 경로)

\2. template 테마 docdash사용 시 docdash다운로드 받아야함 (template는 테마)



![img](https://k.kakaocdn.net/dn/NH3Nf/btqCIE6HFqb/taYwk0y8OFfrwKFT4BGjI1/img.png)jsdoc.conf 생성



```
// jsdoc.conf
{
  "source" : {
    "include" : "./assets/js/layerPopup.js",
    "includePattern" : ".js$"
  },
  "plugins" : [
      "plugins/markdown"
  ],
  "opts" : {
    "template" : "node_modules/docdash",
    "encoding" : "utf8",
    "destination" : "./docs",
    "recurse" : true,
    "verbose" : true
  },
  "templates" : {
    "cleverLinks" : false,
    "monospaceLinks" : false,
    "default" : {
        "outputSourceFiles" : false
    },
    "docdash" : {
      "static" : false,
      "sort" : true
    }
  }
}
```

 

\4. 결과물

```
// cmd
jsdoc -c jsdoc.conf README.md
```

\- jsdoc -c : 참조하는 (설정파일 configuration)

\- jsdoc.conf : 설정파일

\- README.md : readme.md 파일 포함하여 생성

 

 

자동 생성된 docs 폴더에서 index.html 확인

(자동생성되는 폴더의 기본 네이밍은 out이지만 jsdoc.conf 파일에서 docs로 변경하였습니다.)



![img](https://k.kakaocdn.net/dn/J6884/btqCD89lY9k/2knqBgiZ10CluY74sfbe9k/img.png)docs 폴더 구조



 

### 주석 설명

#### 문서 설명 주석

문서를 설명하는 주석으로 문서 상단에 입력하여 문서를 설명한다.

 

**@author**

작성자 식별, 이메일 주소가 있으면 이름 뒤에 꺽쇠괄호로 작성한다.

이메일주소 입력 시에 출력화면에 메일주소가 노출되지는 않으나 앞에 작성한 텍스트(작성자)를 클릭할 경우 mailto 태그처럼 이메일 주소를 식별해준다.

**문법**

```
// @author <name>
// @author <name> [<emailAddress>]
```

**예제**

```
/**
 * @author Jane Smith <jsmith@example.com>
 */

function MyClass() {}
```

**출력화면**



![img](https://k.kakaocdn.net/dn/Hmi2G/btqCBwwcbP9/jOON8eDcAlsriYIAKhsyV0/img.png)출력 이미지



 

**@version** 

라이브러리 버전 정보

**문법**

```
// @version 버전정보
```

**예제**

```
/**
 * Solves equations of the form a * x = b. Returns the value
 * of x.
 * @version 1.2.3
 */

function solver(a, b) {
	return b / a;
}
```

**출력화면**



![img](https://k.kakaocdn.net/dn/bogy4i/btqCF7V3TvQ/M7nq7nnpybVcY1mZJ4srh0/img.png)출력 이미지



 

**@copyright** 

파일 개요, 설명에 대한 저작권 정보 (w.@file)

**문법**

```
// @copyright <some copyright text>
```

 

**@file (@fileoverview, @overview)**

파일에 대한 설명

**문법**

```
// @file <some text>
```

**예제**

```
/**
 * @file This is my cool script.
 * @copyright Michael Mathews 2011
 */
```

**출력화면**



![img](https://k.kakaocdn.net/dn/bqQGit/btqCHxz0rrz/iPMwVKcz0guIQzRrXnAtJ1/img.png)출력 이미지



 

**@license**

소프트웨어 라이센스

표준오픈소스 라이브러리 식별자(identifier) 입력 https://spdx.org/licenses/

**문법**

```
// @license <identifier>
```

**예제**

```
/**
 * Utility functions for the foo package.
 * @module foo/util
 * @license Apache-2.0
 */
```

**예제2**

독립라이센스가 있는 파일

```
/**
 * @license
 * Copyright (c) 2015 Example Corporation Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */
```

**출력화면**



![img](https://k.kakaocdn.net/dn/tdA14/btqCDlnu9TS/3tynM3Ya4rMZDx3cGPVY91/img.png)출력 이미지



####  

#### 함수에 사용할 수 있는 주석

 

**@this**

해당 함수내부의 this가 참조하는 것을 표시

**문법**

```
// @this <namePath>
```

**예제**

```
/** @constructor */
function Greeter(name) {
	setName.apply(this, name);
}

/** @this Greeter */
function setName(name) {
  /** document me */
  this.name = name;
}
```

**출력화면**



![img](https://k.kakaocdn.net/dn/buzxde/btqCFy7rHnl/WcWsuxHJ2kFHLjHd8wqHCk/img.png)출력 이미지



 

**@constant (@const)** 

상수를 표시

**문법**

```
// @constant [<type> <name>]
```

**예시**

```
/**
 * @constant
 * @type {string}
 * @default
 */
const RED = 'FF0000';

/** @constant {number} */
var ONE = 1;
```

 

**@description (@desc)**

설명을 표시

**문법**

```
// @description <some description>
```

**예제**

첫번째 줄일때에는 생략가능

```
/**
 * Add two numbers.
 * @param {number} a
 * @param {number} b
 * @returns {number}
 */
function add(a, b) {
	return a + b;
}
```

**예제2**

첫번째 줄이 아닐때

```
/**
 * @param {number} a
 * @param {number} b
 * @returns {number}
 * @description Add two numbers.
 */
function add(a, b) {
	return a + b;
}
```

**출력화면**



![img](https://k.kakaocdn.net/dn/27gnl/btqCEOip6Oj/9XpUGaTQeKypv10i10ZdxK/img.png)출력 이미지



 

**@throws (@exception)**

메소드에 의해 발생된 오류나 예외사항을 표시

단일 주석에 두번 포함하지말 것

**문법**

```
// @throws free-form description
// @throws {<type>}
// @throws {<type>} free-form description
```

**예제**

```
/**
 * @throws {DivideByZero} Argument x must be non-zero.
 */

function baz(x) {}
```

**출력화면**



![img](https://k.kakaocdn.net/dn/brNIjD/btqCB7XrAhp/xtjKWUUxO76UEUzVyUI8TK/img.png)출력 이미지



 

**@param (@arg, @argument)**

함수에 전달받은 인자 값의 이름

유형 및 설명을 표시

**문법**

```
// @param  <someParamName>
// @param {<type>} <someParamName>
// @param {<type>} <some description>
```

**예제**

단일 속성

```
/**
 * @param {string} somebody - Somebody's name.
 */
function sayHello(somebody) {
	alert('Hello ' + somebody);
}
```

**예제2**

복수 속성

```
/**
 * @param {(string|string[])} [somebody=John Doe] - Somebody's name, or an array of names.
 */
 function sayHello(somebody) {
 	if (!somebody) {
    	somebody = 'John Doe';
    } else if (Array.isArray(somebody)) {
    	somebody = somebody.join(', ');
    }
    
    alert('Hello ' + somebody);
}
```

**예제3**

파라미터에 속성이 있을때

```
/**
 * Assign the project to an employee.
 * @param {Object} employee - The employee who is responsible for the project.
 * @param {string} employee.name - The name of the employee.
 * @param {string} employee.department - The employee's department.
 */
Project.prototype.assign = function(employee) {
	// ...
};
```

**예제4**

파라미터가 배열, 속성이 있을경우

```
/**
 * Assign the project to a list of employees.
 * @param {Object[]} employees - The employees who are responsible for the project.
 * @param {string} employees[].name - The name of an employee.
 * @param {string} employees[].department - The employee's department.
 */
Project.prototype.assign = function(employees) {
	// ...
};
```

**출력화면**



![img](https://k.kakaocdn.net/dn/QqVON/btqCFxAGBI3/5EJethbx94LH0o2FAl8kt0/img.png)출력 이미지



 

**@requires** 

필요한 모듈이 있음을 표현

**문법**

```
// @requires <someModuleName>
```

**예제**

```
/**
 * This class requires the modules {@link module:xyzcorp/helper} and
 * {@link module:xyzcorp/helper.ShinyWidget#polish}.
 * @class
 * @requires module:xyzcorp/helper
 * @requires xyzcorp/helper.ShinyWidget#polish
*/
function Widgetizer() {}
```

**출력화면**



![img](https://k.kakaocdn.net/dn/QUgXd/btqCHw8VCsr/mwGTF2rDZyVgkwogLcJFO1/img.png)출력 이미지



 

**@callback**

콜백으로 받은 인자 및 반환 값에 대한 정보 제공

**문법**

```
// @callback <namepath>
```

**예제**

클래스 별

```
/**
 * @class
 */
function Requester() {}

/**
 * Send a request.
 * @param {Requester~requestCallback} cb - The callback that handles the response.
 */
Requester.prototype.send = function(cb) {
	// code
};

/**
 * This callback is displayed as part of the Requester class.
 * @callback Requester~requestCallback
 * @param {number} responseCode
 * @param {string} responseMessage
 */
```

**예제2**

글로벌

```
/**
 * @class
 */
function Requester() {}

/**
 * Send a request.
 * @param {requestCallback} cb - The callback that handles the response.
 */
Requester.prototype.send = function(cb) {
	// code
};

/**
 * This callback is displayed as a global member.
 * @callback requestCallback
 * @param {number} responseCode
 * @param {string} responseMessage
*/
```

 

**@todo**

해야하거나, 완료해야할 작업이 필요할때 표시

단일 주석에 두번 사용 금지

**문법**

```
// @todo text describing thing to do.
```

**예제**

```
/**
 * @todo Write the documentation.
 * @todo Implement this function.
 */
function foo() {
	// write me
}
```

**출력화면**



![img](https://k.kakaocdn.net/dn/Ln3Z3/btqCB7C67oy/QJHJQpIPr3707iUpEhH7y0/img.png)출력 이미지



 

**@return (@returns)**

함수가 반환하는 값을 표시

**문법**

```
// @returns [{type}] [description]
```

**예제**

```
/**
 * Returns the sum of a and b
 * @param {number} a
 * @param {number} b
 * @returns {number} Sum of a and b
 */
function sum(a, b) {
	return a + b;
}
```

**출력화면**



![img](https://k.kakaocdn.net/dn/crHguh/btqCD8nWuti/v18dkZJqIqjoVHKOKhypG1/img.png)출력이미지



 

**@see**

연관성 있는 문서나 리소스 참조함을 표시

{@link} 와 같이 사용 가능

**문법**

```
// @see <namepath>
// @see <text>
```

**예제**

```
/**
 * Both of these will link to the bar function.
 * @see {@link bar}
 * @see bar
 */
function foo() {}

// Use the inline {@link} tag to include a link within a free-form description.
/**
 * @see {@link foo} for further information.
 * @see {@link http://github.com|GitHub}
 */
function bar() {}
```

**출력화면**



![img](https://k.kakaocdn.net/dn/cYWPmx/btqCDlHIaDb/2MUXBIdk1ez4kdugZbWIOk/img.png)출력이미지



 

**@link ({@linkcode}, {@linkplain})**

namepath 또는 url에 대한 링크 생성

**문법**

```
// {@link namepathOrURL}
// [link text]{@link namepathOrURL}
// {@link namepathOrURL|link text}
// {@link namepathOrURL link text (after the first space)}
```

**예제**

```
/*
 ** See {@link MyClass} and [MyClass's foo property]{@link MyClass#foo}.
 * Also, check out {@link http://www.google.com|Google} and
 * {@link https://github.com GitHub}.
 */
function myFunction() {}
```

 

**@since**

클래스, 메서드 등이 특정 버전에서 추가되었을때 사용

**문법**

```
// @since <versionDescription>
```

**예제**

```
/**
 * Provides access to user information.
 * @since 1.0.1
 */
function UserRecord() {}
```

**출력화면**



![img](https://k.kakaocdn.net/dn/cSzO4h/btqCF7V29pT/KQi5TRXhhDeQvX0n1gGBaK/img.png)출력이미지



 

이벤트

**@fires | @event | @listens**

 

**@fires (@emits)**

메소드가 호출 될 때

지정된 유형의 이벤트를 발생시킬 수 있음을 표현

**문법**

```
// @fires <className>#<eventName>
// @fires <className>#[event:]<eventName>
```

 

**@event**

특정 이벤트를 정의

**문법**

```
// @event <className>#<eventName>
// @event <className>#[event:]<eventName>
```

 

**@listens**

지정된 이벤트를 수신하는 것을 표현

**문법**

```
// @listens <eventName>
```

**예제**

```
define('hurler', [], function () {
  /**
   * Event reporting that a snowball has been hurled.
   *
   * @event module:hurler~snowball
   * @property {number} velocity - The snowball's velocity, in meters per second.
   */

  /**
   * Snowball-hurling module.
   *
   * @module hurler
   */
  var exports = {
    /**
     * Attack an innocent (or guilty) person with a snowball.
     *
     * @method
     * @fires module:hurler~snowball
     */
    attack: function () {
    	this.emit('snowball', { velocity: 10 });
    }
  }; 
  
  return exports;  
});
  
define('playground/monitor', [], function () {
    /**
     * Keeps an eye out for snowball-throwers.
     *
     * @module playground/monitor
     */
    var exports = {
      /**
       * Report the throwing of a snowball.
       *
       * @method
       * @param {module:hurler~event:snowball} e - A snowball event.
       * @listens module:hurler~event:snowball
       */
      reportThrowage: function (e) {
          this.log('snowball thrown: velocity ' + e.velocity);
      }
    }; 
    
    return exports;
});
```

 

**@example**

예제 제공

<caption>태그를 @example 뒤에 사용하여 캡션기능 제공 가능

**문법**

```
// @example 
// @exmple <caption>captionText</caption>
```

**예제**

```
/**
 * Solves equations of the form a * x = b
 * @example
 * // returns 2
 * @example <caption>Example usage of method1.</caption>
 * // returns 2
 * globalNS.method1(5, 10);
 * @returns {Number} Returns the value of x for the equation.
 */
globalNS.method1 = function (a, b) {
	return b / a;
};
```

**출력화면**



![img](https://k.kakaocdn.net/dn/cCTWy7/btqCEOpbWGi/JDlbGeEO1uWVGn6dX5m8w0/img.png)출력이미지



 

**@global**

전역함수 표현, 로컬에 작성되고 전역에 할당된 태그 사용에 유용

**예제**

```
(function() {
  /** @global */
  var foo = 'hello foo';
  this.foo = foo;
}).apply(window);
```

**출력화면**



![img](https://k.kakaocdn.net/dn/kJcur/btqCID02ABd/G1uIRbbvMMaznup585lDzk/img.png)출력 이미지



 

**@namespace**

네임스페이스 프로그래밍 시 객체 표현

**문법**

```
// @namespace [[{<type>}] <SomeName>]
```

**예제**

```
/**
 * My namespace.
 * @namespace
 */
var MyNamespace = {
  /** documented as MyNamespace.foo */
  foo: function() {},
  
  /** documented as MyNamespace.bar */
  bar: 1
};
```

**예제2**

```
/**
 * A namespace.
 * @namespace MyNamespace
 */

/**
 * A function in MyNamespace (MyNamespace.myFunction).
 * @function myFunction
 * @memberof MyNamespace
 */
```

**예제3**

```
/** @namespace window */
/**
 * Shorthand for the alert function.
 * Refer to it as {@link window."!"} (note the double quotes).
 */
window["!"] = function(msg) { 
	alert(msg); 
};
```

 

**@inner**

네임스페이스 태그의 부모-자녀 참조

**예제**

```
/** @namespace */
var MyNamespace = {
  /**
   * foo is now MyNamespace~foo rather than MyNamespace.foo.
   * @inner
   */
  foo: 1
};
```

 

**@alias**

네임스페이스 태그의 멤버 참조처리

내부 함수 내에 클래스 정의할 때 유용하다

**예제**

```
/** @namespace */
var Apple = {};(function(ns) {

  /**
   * @namespace
   * @alias Apple.Core
   */
  var core = {}; 

  /** Documented as Apple.Core.seed */
  core.seed = function() {}; 
  ns.Core = core;

})(Apple);
```

####  

#### 클래스를 설명하는 주석

class 키워드를 사용했거나 생성자를 통해 개발한 경우 해당할 수 있습니다.

 

**@class (@constructor)**

함수 생성자로 표시

**문법**

```
// @class [<type> <name>]
```

**예제**

```
/**
 * Creates a new Person.
 * @class
 */
function Person(){}
var p = new Person();
```

**출력화면**



![img](https://k.kakaocdn.net/dn/b1Z7Hq/btqCIDUf7pG/7TjaUjGHzFXXf1WSKdkaT1/img.png)출력이미지



 

 

**@classdesc**

함수 생성자 설명

@class가 선언되어있어야 한다.

**문법**

```
// @classdesc <some description>
```

**예제**

```
/**
 * This is a description of the MyClass constructor function. 
 * @class
 * @classdesc This is a description of the MyClass class.
 */
function MyClass() {}
```

**출력화면**



![img](https://k.kakaocdn.net/dn/v10dk/btqCF6pnGNA/5zKkBPoX43Mmffe4pcz8QK/img.png)출력 이미지



 

**@constructs**

객체리터럴를 사용하여 클래스를 정의했을때 해당 멤버 표시

@lends와 사용할 수 있다.

**문법**

```
// @constructs [<name>]
```

**예제**

```
makeClass('Menu',
  /**
   * @constructs Menu
   * @param items
   */
  function (items){},
  {
    /** @memberof Menu# */
    show: function(){}
  }
);

// @lends와 사용
var Person = makeClass(
  /** @lends Person.prototype */
  {
    /** @constructs */
    initialize: function(name) {
        this.name = name;
    },
    /** Describe me. */
    say: function(message) {
        return this.name + " says: " + message;
    }
  }
);
```

**출력화면**



![img](https://k.kakaocdn.net/dn/N0PcY/btqCBxIFc3C/B3HrdbvZxklpNHy3bFLS11/img.png)출력이미지



 

**@lends** 

함수 생성자의 멤버

**문법**

```
// @lends <namepath>
```

**예제**

```
/** @class */
var Person = makeClass(
  /** @lends Person */
  {
    /**
     * Create a `Person` instance.
     * @param {string} name - The person's name.
     */
    initialize: function(name) {
        this.name = name;
    },
    /**
     * Say something.
     * @param {string} message - The message to say.
     * @returns {string} The complete message.
     */
    say: function(message) {
        return this.name + " says: " + message;
    }
  }
);
```

 

**@abstract (@virtual)**

상속하는 객체에서 재정의하는 멤버 식별(오버라이딩 객체)

**예제**

```
/**
 * Generic dairy product.
 * @constructor
 */
function DairyProduct() {}

/**
 * Check whether the dairy product is solid at room temperature.
 * @abstract
 * @return {boolean}
 */
DairyProduct.prototype.isSolid = function() {
	throw new Error('must be implemented by subclass!');
};

/**
 * Cool, refreshing milk.
 * @constructor
 * @augments DairyProduct
 */
function Milk() {}

/**
 * Check whether milk is solid at room temperature.
 * @return {boolean} Always returns false.
 */
Milk.prototype.isSolid = function() {
	return false;
};
```

**출력화면**



![img](https://k.kakaocdn.net/dn/bf5wjM/btqCFyM890w/c7qKXpAAzS1P1RcGgDoKOK/img.png)출력이미지



 

**@augments (@extends)**

클래스 기반이나 프로토타입 기반에서 상속을 나타내고 상위 객체를 추가함

**문법**

```
// @augments <namepath>
```

**예제**

단일상속

```
/**
 * @constructor
 */
function Animal() {
	/** Is this animal alive? */
	this.alive = true;
}

/**
 * @constructor
 * @augments Animal
 */
function Duck() {}
Duck.prototype = new Animal();
```

**예제2**

다중 상속

```
/**
 * Abstract class for things that can fly.
 * @class
 */
function Flyable() {
	this.canFly = true;
}

/** Take off. */
Flyable.prototype.takeOff = function() {
	// ...
};

/**
 * Abstract class representing a bird.
 * @class
 */
function Bird(canFly) {
	this.canFly = canFly;
}

/** Spread your wings and fly, if possible. */
Bird.prototype.takeOff = function() {
  if (this.canFly) {
    this._spreadWings()
    ._run()
    ._flapWings();
  }
};

/**
 * Class representing a duck.
 * @class
 * @augments Flyable
 * @augments Bird
 */
function Duck() {} // Described in the docs as "Spread your wings and fly, if possible."
Duck.prototype.takeOff = function() {
	// ...
};
```

 

주석 정리 후 모듈에 적용을 해봤는데, 아직 정확한 개념이 박히지 않아서 오래걸리는군요 ㅎㅎ..

개발 시 주석을 잘 달기 위해 다른 문서화 도구들도 봐야할 것 같습니다.


