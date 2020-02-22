---
title: "리엑트 리덕스  : Class기반 리덕스 기초"
sub_title: "카운터 웹"
categories:
  - redux
  - react
  - react redux
elements:
  - content
  - css
  - formatting
  - html
  - markup
last_modified_at: 2020-02-23 T20:16:49-05:00
---

## react redux class 기반과 함수 기반 에서 구현

#### 1. class 기반으로 기초를 구현한 후 그것을 함수기반으로 바꿔보자

0. ##### 구조

   - 리덕스를 이용해  + 버튼을 누려면  1씩 증가하고 - 버튼을 누루면 1씩 감소하는 

     Counter Web을 리엑트를 이용해 만들어 보자 

   

1. 프로젝트 명을 정하고 설치하기 

   ```powershell
   npx create-react-app react-redux-counter
   cd react-redux-counter
   code . 
   -> vscode를 활용해서 편집
   ```

   react-redux-counter 디렉토리에 들어가 필요한 모듈을 설치 

   ```javascript
   npm install redux react-redux
   ```

   

2. 화면 구성하기 

   1. components 폴더 생성후 Counter.js를 새로 만들고 다음과 같이 코딩한다.

    

   ```javascript
   import React from 'react' ;
   const Counter = () => {
     return (
       <div>
         <h1>myCounter</h1> 
         <button>+</button> 
         <button>-</button> 
       </div>
     ) ;
   } ;
   
   ```

   2. App.js 수정

   ```javascript
   import React, { Component } from 'react';
   
   import './App.css';
   import Counter from './components/Counter';
   
   class App extends Component {
     render() {
       return (
         <div className="App">
           <Counter  />
         </div>
       );
     }
   }
   
   export default App;
   ```

   <img width="1088" alt="스크린샷 2020-02-22 오후 6 39 11" src="https://user-images.githubusercontent.com/25717861/75091310-38467200-55af-11ea-9850-81b2e100f30e.png">

   위와 같은 부분이 나탄난다.

   ### 3. Action

   ##### 액션: 상태 변화를 일으킬 때 참조하는 객체.

   우리는 Counter 값을 변화시키는데 + 버튼, - 버튼을 이용하여 증.감소를 합니다.

   그럼 만들어야할 액션은 두가지 + 버튼, -버튼입니다.

   ```
   * Store에 대해 뭔가 하고싶은 경우에 Action을 발행한다.
   * Store의 문지기(Reducer)가 Action을 감지하면, 새로운 State가 생긴다.
   ```

   

   1. ##### /src/reducers/counter.js 생성

   ```javascript
   // 액션 타입 정의
   const INCREMENT = 'INCREMENT' ;
   const DECREMENT = 'DECREMENT' ;
   
   // 액션 생성 함수 정의
   export const increment = () => ({ type: INCREMENT }) ;
   export const decreuemt = () => ({ type: DECREMENT }) ;
   
   // 초기 상태 정의
   const initialState = {
       number: 0
   } ;
   ```

   

   ![image](https://user-images.githubusercontent.com/25717861/75091317-42687080-55af-11ea-8aed-bdd96b05aad0.png)

###  4. 리듀서 작성

#####      리듀서는 상태에 변화를 일으키는 함수로써 리듀서는 파라미터를 두 개를 받습니다.

##### 	 첫번째 파라미터는 현재상태이고, 두번째 파라미터는 액션 객체입니다.

###### 	1. /src/reducers/counter.js 에 다음코드 추가

​		

```javascript
// 리듀서 작성
export default function Counter(state=initialState, action) {
    switch(action.type) {
        case INCREMENT:
            return {
                ...state,
                number: state.number + 1 ,
            } ;
        case DECREMENT:
            return {
                ...state,
                number: state.number - 1,
            } ;
        default:
            return state ;
    }
}
```



![image (1)](https://user-images.githubusercontent.com/25717861/75091344-7b084a00-55af-11ea-9185-3be55de1a6be.png)

##### 	2. src/reducers/index.js

​		

```javascript
import { combineReducers } from 'redux' ;
import counter from './counter' ;

const rootReducer = combineReducers({
    counter,
    //다른 리듀서를 만들게 되면 여기에 import
}) ;

export default rootReducer;
```



### 5. 스토어 만들기

#### 	스토어는 하나의 애플리케이션 에는 하나의 스토어가 있다.

##### 	1. src/index.js

​		

```javascript
import React from 'react';
import ReactDOM from 'react-dom';
// createStore 와 루트 리듀서 불러오기
import { createStore } from 'redux';
import rootReducer from './reducers';
import { Provider } from 'react-redux' ;
import * as serviceWorker from './serviceWorker';

import './index.css';
import App from './App';


// **** 리덕스 개발자 도구 적용
const devTools =
  window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__();
const store = createStore(rootReducer, devTools);

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById('root')
);

serviceWorker.unregister()
```



```
import { createStore } from 'redux';
```

createStore를 가져와서 지금까지 reducer를 인자로 받는다.

```
const store = createStore(rootReducer, devTools);
```



devTools 부분은 초기 상태값들 나타 낼 수 있다.

### 6. 지금까지 한 부분 정리 및 해야 할 일

​	여기까지 정리하자면 우리는 화면(Counter.js) 에서 +,- 버튼을 클릭하게 되면 액션을 통해 리듀서를(counter.js) 거치고 스토어 상태를 변화한 후 다시 view에 변화를 주어야한다.

```null
우리가 한 일은
1. 화면생성 (Counter.js)
2. 액션생성 (counter.js)
3. 리듀서 생성(counter.js)
4. 스토어 생성(index.js)
```

이렇게하면 다 된 것 같지만 여기서 몇까지 빼먹은 것이 있다.!

앞으로 해야 할 일!!!

```null
1. 액션을 스토어에 전달하는 역할인 dispatch 생성 (mapDispatchToProps)
2. store에 state를 view에 전달해주기 (mapStateToProps)
3. store와 reducer를 연결시킬 수 있도록 만들어진 Component 생성 (CounterContainter.js)
4. 위의 두가지가 적용된 props를 받을 수 있는 component를 정의 (App.js)
```



### 7. 해야할 일 1 ,2 ,3 을 생성

##### 	1. src/components/Counter.js 를 화면에 보여질때 나오는 변화되는 값들을 보여주기 위해서 

##### 		다음과 같이 수정하기.

​		

```javascript
import React from 'react' ;

const Counter = ({ value, onIncrement, onDecrement }) => {
  return (
    <div>
      <h1>{value}</h1>
      <button onClick={onIncrement}>+</button>
      <button onClick={onDecrement}>-</button>
    </div>
  ) ;
} ;

export default Counter ;
```





컴포넌트에 리덕스 스토어 안에 있는 값이나 액션 함수들을 연결해주어야 한다.
리덕스와 연동된 컴포넌트를 우리는 컨테이너 컴포넌트라고 라고 한다.

그러기 위해 react-redux에 있는 connect 매서드를 사용해서 mapStateToProps,
    mapDispatchToProps 등을 인자로 받고 다시 컨테이너 컴포넌트와 연결하여 준다.

#### 	2.src/components/CounterContainer.js 

```javascript
import React, { Component } from 'react';
import { connect } from 'react-redux';
import Counter from '../components/Counter';
import { increment, decrement } from '../reducers/counter';

class CounterContainer extends Component { //3
    handleIncrement = () => {
        this.props.increment() ;
    } ;

    handleDecrement = () => {
        this.props.decrement () ;
    } ;

    render() {
        const { number } = this.props ;
        return (
            <Counter 
                value={number}
                onIncrement={this.handleIncrement}
                onDecrement={this.handleDecrement}
            />
        ) ;
    } 
}


const mapStateToProps = ({ counter }) => ({  //2
    number: counter.number,
}) ;

const mapDispatchToProps = {increment, decrement} ; //1

export default connect ( // 스토어와 연결
    mapStateToProps,
    mapDispatchToProps
)(CounterContainer) ;
```



마지막으로 App.js에서 CounterContainer컴퍼넌트를 호출 한다.

<img width="1097" alt="스크린샷 2020-02-22 오후 7 49 00" src="https://user-images.githubusercontent.com/25717861/75091309-35e41800-55af-11ea-96ac-ae9805a7354d.png">

