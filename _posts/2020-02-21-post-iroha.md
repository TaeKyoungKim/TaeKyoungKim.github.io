# 1. 이로 하 개요 

## 1.1. 이로 하의 주요 특징은 무엇입니까? 

- 간단한 배포 및 유지 관리
- 개발자를위한 다양한 라이브러리
- 역할 기반 액세스 제어
- 명령-쿼리 분리 원리에 의해 구동되는 모듈 식 설계
- 자산 및 신원 관리

다음에 중점을두고 지속적으로 모델을 개선합니다.

- 신뢰성 (내결함성, 복 구성)
- 성능 효율성 (특히 시간 동작 및 리소스 활용)
- 사용성 (학습 성, 사용자 오류 방지, 적합성 인식 성)

## 1.2. Iroha는 어디에서 사용할 수 있습니까? 

Hyperledger Iroha는 디지털 자산, 신원 및 직렬화 된 데이터를 관리하는 데 사용할 수있는 범용 허가 블록 체인 시스템입니다. 이는 은행 간 결제, 중앙 은행 디지털 통화, 지불 시스템, 국가 ID 및 물류와 같은 애플리케이션에 유용 할 수 있습니다.

자세한 설명은 [사용 사례 시나리오 섹션을](https://iroha.readthedocs.io/en/latest/develop/cases.html) 확인 [하십시오](https://iroha.readthedocs.io/en/latest/develop/cases.html) .

## 1.3. 비트 코인이나 이더 리움과 어떻게 다릅니 까? 

비트 코인과 이더 리움은 누구나 데이터에 합류하고 액세스 할 수있는 권한이없는 원장으로 설계되었습니다. 또한 시스템과 상호 작용하는 데 필요한 기본 암호 화폐가 있습니다.

Iroha에는 기본 암호 화폐가 없습니다. 대신 기업의 요구를 충족시키기 위해 시스템 상호 작용이 허용됩니다. 즉, 필요한 액세스 권한이있는 사람 만 시스템과 상호 작용할 수 있습니다. 또한 모든 데이터에 대한 액세스를 제어 할 수 있도록 쿼리도 허용됩니다.

특히 Ethereum과의 주요 차이점 중 하나는 Hyperledger Iroha를 사용하면 시스템에있는 사전 빌드 된 명령을 사용하여 디지털 자산 작성 및 전송과 같은 공통 기능을 수행 할 수 있다는 것입니다. 따라서 성가신 계약을 작성하기가 까다 롭고 스마트 계약을 테스트 할 필요가 없으므로 개발자는 간단한 작업을 더 빠르고 위험없이 완료 할 수 있습니다.

## 1.4. 다른 Hyperledger 프레임 워크 또는 다른 허가 된 블록 체인과 어떻게 다릅니 까? 

Iroha에는 고성능이며 지연 시간이 짧은 트랜잭션의 최종성을 허용하는 새로운 충돌 내결함성 합의 알고리즘 (YAC [[1\]](https://iroha.readthedocs.io/en/latest/overview.html#f1) )이 있습니다.

또한 Iroha의 기본 제공 명령은 다른 플랫폼에 비해 주요 이점입니다. 디지털 자산 생성, 계정 등록 및 계정간에 자산 전송과 같은 일반적인 작업을 수행하는 것이 매우 간단하기 때문입니다. 또한, 공격 벡터를 좁히고 실패 할 일이 적기 때문에 시스템의 전반적인 보안을 향상시킵니다.

마지막으로, Iroha는 강력한 권한 시스템을 가진 유일한 원장으로, 네트워크의 모든 명령, 쿼리 및 조인에 대한 권한을 설정할 수 있습니다.

| [[1\]](https://iroha.readthedocs.io/en/latest/overview.html#id1) | 또 다른 합의 |
| ------------------------------------------------------------ | :----------- |
|                                                              |              |

## 1.5. Iroha를 중심으로 응용 프로그램을 만드는 방법은 무엇입니까? 

블록 체인의 힘을 응용 프로그램에 적용하려면 먼저 Iroha 피어와 인터페이스하는 방법을 생각해야합니다. 트랜잭션과 쿼리가 정확히 무엇인지, 응용 프로그램 사용자가 어떻게 상호 작용해야하는지 설명하는 [개념 및 아키텍처 섹션](https://iroha.readthedocs.io/en/latest/concepts_architecture/index.html) 을 확인하는 것이 좋습니다 .

또한 개발자가 서명, 명령, Iroha 동료에게 메시지를 보내고 상태를 확인하는 등 빌딩 블록을 구성 할 수있는 도구를 제공하는 여러 클라이언트 라이브러리가 있습니다.