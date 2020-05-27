# 패브릭 테스트 네트워크 사용

Hyperledger Fabric Docker 이미지 및 샘플을 다운로드 한 후 `fabric-samples`저장소에 제공된 스크립트를 사용하여 테스트 네트워크를 배치 할 수 있습니다 . 테스트 네트워크를 사용하여 로컬 시스템에서 노드를 실행하여 패브릭에 대해 배울 수 있습니다. 숙련 된 개발자는 네트워크를 사용하여 스마트 계약 및 애플리케이션을 테스트 할 수 있습니다. 네트워크는 교육 및 테스트 도구로만 사용해야합니다. 프로덕션 네트워크를 배포하기위한 템플릿으로 사용해서는 안됩니다. 테스트 네트워크는 `first-network`샘플을 장기적으로 대체하기 위해 Fabric v2.0에 도입되었습니다 .

샘플 네트워크는 Docker Compose를 사용하여 패브릭 네트워크를 배포합니다. 노드는 Docker Compose 네트워크 내에서 격리되므로 테스트 네트워크는 실행중인 다른 패브릭 노드에 연결하도록 구성되지 않았습니다.

**참고 :** 이 지시 사항은 안정된 최신 Docker 이미지 및 제공된 tar 파일 내의 사전 컴파일 된 설정 유틸리티에 대해 작동하는 것으로 확인되었습니다. 현재 마스터 브랜치의 이미지 또는 도구를 사용하여 이러한 명령을 실행하면 오류가 발생할 수 있습니다.



## 시작하기 전에

테스트 네트워크를 실행하기 전에 `fabric-samples` 저장소 를 복제 하고 패브릭 이미지를 다운로드 해야합니다 . [전제 조건](https://hyperledger-fabric.readthedocs.io/en/release-2.0/prereqs.html) 을 [설치하고 샘플, 바이너리 및 Docker 이미지를](https://hyperledger-fabric.readthedocs.io/en/release-2.0/install.html) 설치했는지 확인하십시오 .



## 테스트 네트워크를 시작하십시오

저장소 `test-network`디렉토리 에서 네트워크를 불러오는 스크립트를 찾을 수 있습니다 `fabric-samples`. 다음 명령을 사용하여 테스트 네트워크 디렉토리로 이동하십시오.

```
cd fabric-samples/test-network
```

이 디렉토리에서 `network.sh`로컬 시스템의 Docker 이미지를 사용하여 Fabric 네트워크를 나타내는 주석이 달린 스크립트를 찾을 수 있습니다 . 스크립트 도움말 텍스트를 인쇄하기 위해 실행할 수 있습니다 .`./network.sh -h`

```
Usage:
  network.sh <Mode> [Flags]
    <Mode>
      - 'up' - bring up fabric orderer and peer nodes. No channel is created
      - 'up createChannel' - bring up fabric network with one channel
      - 'createChannel' - create and join a channel after the network is created
      - 'deployCC' - deploy the fabcar chaincode on the channel
      - 'down' - clear the network with docker-compose down
      - 'restart' - restart the network

    Flags:
    -ca <use CAs> -  create Certificate Authorities to generate the crypto material
    -c <channel name> - channel name to use (defaults to "mychannel")
    -s <dbtype> - the database backend to use: goleveldb (default) or couchdb
    -r <max retry> - CLI times out after certain number of attempts (defaults to 5)
    -d <delay> - delay duration in seconds (defaults to 3)
    -l <language> - the programming language of the chaincode to deploy: go (default), javascript, or java
    -v <version>  - chaincode version. Must be a round number, 1, 2, 3, etc
    -i <imagetag> - the tag to be used to launch the network (defaults to "latest")
    -verbose - verbose mode
  network.sh -h (print this message)

 Possible Mode and flags
  network.sh up -ca -c -r -d -s -i -verbose
  network.sh up createChannel -ca -c -r -d -s -i -verbose
  network.sh createChannel -c -r -d -verbose
  network.sh deployCC -l -v -r -d -verbose

 Taking all defaults:
    network.sh up

 Examples:
  network.sh up createChannel -ca -c mychannel -s couchdb -i 2.0.0
  network.sh createChannel -c channelName
  network.sh deployCC -l javascript
```

`test-network`디렉토리 내부에서 다음 명령을 실행하여 이전 실행에서 컨테이너 또는 아티팩트를 제거하십시오.

```
./network.sh down
```

그런 다음 다음 명령을 실행하여 네트워크를 불러올 수 있습니다. 다른 디렉토리에서 스크립트를 실행하려고하면 문제가 발생합니다.

```
./network.sh up
```

이 명령은 하나의 주문 노드 인 두 개의 피어 노드로 구성된 패브릭 네트워크를 작성합니다. 우리가 [앞으로 나아갈](https://hyperledger-fabric.readthedocs.io/en/release-2.0/test_network.html#creating-a-channel) 수있을지라도, 당신이 달리면 채널이 생성되지 않습니다 . 명령이 성공적으로 완료되면 작성중인 노드의 로그가 표시됩니다.`./network.sh up`

```
Creating network "net_test" with the default driver
Creating volume "net_orderer.example.com" with default driver
Creating volume "net_peer0.org1.example.com" with default driver
Creating volume "net_peer0.org2.example.com" with default driver
Creating orderer.example.com    ... done
Creating peer0.org2.example.com ... done
Creating peer0.org1.example.com ... done
CONTAINER ID        IMAGE                               COMMAND             CREATED             STATUS                  PORTS                              NAMES
8d0c74b9d6af        hyperledger/fabric-orderer:latest   "orderer"           4 seconds ago       Up Less than a second   0.0.0.0:7050->7050/tcp             orderer.example.com
ea1cf82b5b99        hyperledger/fabric-peer:latest      "peer node start"   4 seconds ago       Up Less than a second   0.0.0.0:7051->7051/tcp             peer0.org1.example.com
cd8d9b23cb56        hyperledger/fabric-peer:latest      "peer node start"   4 seconds ago       Up 1 second             7051/tcp, 0.0.0.0:9051->9051/tcp   peer0.org2.example.com
```

이 결과를 얻지 못하면 [문제 해결](https://hyperledger-fabric.readthedocs.io/en/release-2.0/test_network.html#troubleshooting) 로 넘어 가서 잘못된 [문제에](https://hyperledger-fabric.readthedocs.io/en/release-2.0/test_network.html#troubleshooting) 대한 도움을 받으십시오. 기본적으로 네트워크는 암호화 도구를 사용하여 네트워크를 불러옵니다. 그러나 [인증 기관으로 네트워크를 불러올](https://hyperledger-fabric.readthedocs.io/en/release-2.0/test_network.html#bring-up-the-network-with-certificate-authorities) 수도 있습니다 .



### 테스트 네트워크의 구성 요소

테스트 네트워크가 배포 된 후 구성 요소를 검사하는 데 시간이 걸릴 수 있습니다. 다음 명령을 실행하여 시스템에서 실행중인 모든 Docker 컨테이너를 나열하십시오. `network.sh`스크립트에 의해 작성된 세 개의 노드가 표시되어야합니다 .

```
docker ps -a
```

Fabric 네트워크와 상호 작용하는 각 노드와 사용자는 네트워크 구성원 인 조직에 속해야합니다. Fabric 네트워크의 구성원 인 조직 그룹을 종종 컨소시엄이라고합니다. 테스트 네트워크에는 Org1과 Org2의 두 컨소시엄 멤버가 있습니다. 네트워크에는 네트워크의 주문 서비스를 유지 관리하는 하나의 주문자 조직도 포함됩니다.

[피어](https://hyperledger-fabric.readthedocs.io/en/release-2.0/peers/peers.html) 는 모든 Fabric 네트워크의 기본 구성 요소입니다. 피어는 블록 체인 원장을 저장하고 장부에 커밋되기 전에 트랜잭션을 확인합니다. 피어는 블록 체인 원장의 자산을 관리하는 데 사용되는 비즈니스 논리가 포함 된 스마트 계약을 실행합니다.

네트워크의 모든 동료는 컨소시엄의 구성원에 속해야합니다. 테스트 네트워크에서 각 조직은 하나가 각 피어, 운영 `peer0.org1.example.com` 및 `peer0.org2.example.com`.

모든 Fabric 네트워크에는 [주문 서비스](https://hyperledger-fabric.readthedocs.io/en/release-2.0/orderer/ordering_service.html) 도 포함됩니다 . 피어는 트랜잭션을 확인하고 블록 체인 원장에 트랜잭션 블록을 추가하지만 트랜잭션 순서를 결정하거나 새 블록에 포함시키지 않습니다. 분산 네트워크에서 피어는 서로 멀리 떨어져 실행 중일 수 있으며 트랜잭션이 생성 된 시점에 대한 일반적인 시각을 갖지 않을 수 있습니다. 거래 순서에 대한 합의는 동료들에게 오버 헤드를 발생시키는 비용이 많이 드는 프로세스입니다.

주문 서비스를 통해 피어는 트랜잭션 유효성 검사 및 원장에게 커밋하는 데 집중할 수 있습니다. 주문 노드는 클라이언트로부터 승인 된 트랜잭션을 수신 한 후 트랜잭션 순서에 대해 합의한 다음 블록에 추가합니다. 그런 다음 블록은 피어 노드에 배포되어 블록 체인 원장 블록을 추가합니다. 주문 노드는 또한 블록을 만드는 방법 및 노드가 사용할 수있는 Fabric 버전과 같은 Fabric 네트워크의 기능을 정의하는 시스템 채널을 운영합니다. 시스템 채널은 컨소시엄의 구성원 인 조직을 정의합니다.

샘플 네트워크는 주문 조직에서 운영하는 단일 노드 Raft 주문 서비스를 사용합니다. 머신에서 주문 노드를로 볼 수 있습니다 `orderer.example.com`. 테스트 네트워크는 단일 노드 주문 서비스 만 사용하지만 실제 네트워크에는 하나 또는 여러 주문 조직이 운영하는 여러 주문 노드가 있습니다. 다른 주문 노드는 Raft 합의 알고리즘을 사용하여 네트워크에서 트랜잭션 순서에 동의합니다.



## 채널 만들기

머신에서 피어 및 주문자 노드가 실행 중이므로 스크립트를 사용하여 Org1과 Org2 간의 트랜잭션에 대한 패브릭 채널을 작성할 수 있습니다. 채널은 특정 네트워크 구성원 간의 개인 통신 계층입니다. 채널은 채널에 초대되고 네트워크의 다른 회원에게는 보이지 않는 조직 만 사용할 수 있습니다. 각 채널에는 별도의 블록 체인 원장이 있습니다. 초대 된 조직은 채널 원장을 저장하고 채널에서 트랜잭션을 확인하기 위해 동료를 채널에 "가입"합니다.

이 `network.sh`스크립트를 사용하여 Org1과 Org2 사이에 채널을 만들고 해당 피어를 채널에 가입시킬 수 있습니다. 기본 이름이 다음과 같은 채널을 만들려면 다음 명령을 실행하십시오 `mychannel`.

```
./network.sh createChannel
```

명령이 성공하면 다음 메시지가 로그에 인쇄 된 것을 볼 수 있습니다.

```
========= Channel successfully joined ===========
```

채널 플래그를 사용하여 맞춤 이름으로 채널을 만들 수도 있습니다. 예를 들어 다음 명령은 다음과 같은 이름의 채널을 만듭니다 `channel1`.

```
./network.sh createChannel -c channel1
```

채널 플래그를 사용하면 다른 채널 이름을 지정하여 여러 채널을 만들 수도 있습니다. 당신이 만든 후에 `mychannel`또는 `channel1`라는 이름의 두 번째 채널을 만들려면 아래, 당신은 명령을 사용할 수 있습니다 `channel2`:

```
./network.sh createChannel -c channel2
```

네트워크를 불러오고 한 단계로 채널을 만들려면 `up`및 `createChannel`모드를 함께 사용할 수 있습니다 .

```
./network.sh up createChannel
```



## 채널에서 체인 코드 시작

채널을 만든 후 [스마트 계약](https://hyperledger-fabric.readthedocs.io/en/release-2.0/smartcontract/smartcontract.html) 을 사용하여 채널 원장과 상호 작용할 수 있습니다 . 스마트 계약에는 블록 체인 원장의 자산을 관리하는 비즈니스 로직이 포함되어 있습니다. 네트워크 구성원이 실행하는 응용 프로그램은 스마트 계약을 호출하여 원장에 자산을 생성하고 해당 자산을 변경 및 전송할 수 있습니다. 응용 프로그램은 또한 스마트 계약을 쿼리하여 원장의 데이터를 읽습니다.

트랜잭션이 유효하도록하려면 스마트 계약을 사용하여 생성 된 트랜잭션은 일반적으로 여러 조직에서 서명하여 채널 원장에 커밋해야합니다. 여러 서명은 Fabric의 트러스트 모델에 필수적입니다. 거래에 대해 여러 보증을 요구하면 채널의 한 조직이 동료의 원장을 변경하거나 동의하지 않은 비즈니스 로직을 사용하지 못하게됩니다. 거래에 서명하려면 각 조직이 동료에 대해 스마트 계약을 호출하고 실행 한 다음 거래 결과에 서명해야합니다. 출력이 일관되고 충분한 조직이 서명 한 경우 거래를 원장에게 맡길 수 있습니다. 스마트 계약을 실행해야하는 채널의 세트 조직을 지정하는 정책을 보증 정책이라고합니다.

Fabric에서 스마트 계약은 체인 코드라고하는 패키지로 네트워크에 배포됩니다. 체인 코드는 조직의 피어에 설치된 다음 채널에 배포되며, 트랜잭션을 승인하고 블록 체인 원장과 상호 작용하는 데 사용할 수 있습니다. 체인 코드를 채널에 배포하려면 채널 구성원이 체인 코드 거버넌스를 설정하는 체인 코드 정의에 동의해야합니다. 필요한 수의 조직이 동의하면 체인 코드 정의를 채널에 커밋하고 체인 코드를 사용할 수 있습니다.

를 사용 `network.sh`하여 채널을 만든 후 다음 명령을 사용하여 채널에서 체인 코드를 시작할 수 있습니다.

```
./network.sh deployCC
```

`deployCC`부속 명령은 설치됩니다 **fabcar의** 에 chaincode을 `peer0.org1.example.com`하고 `peer0.org2.example.com`다음 채널 플래그를 사용하여 지정된 채널 (또는에 chaincode를 배포 `mychannel` 어떤 채널이 지정되지 않은 경우). 체인 코드를 처음 배포하는 경우 스크립트는 체인 코드 종속성을 설치합니다. 기본적으로 스크립트는 Fab 버전의 Gocar 버전을 설치합니다. 그러나 언어 플래그 ( `-l`)를 사용하여 Java 또는 Javascript 버전의 체인 코드를 설치할 수 있습니다 . 디렉토리 의 `chaincode`폴더 에서 Fabcar 체인 코드를 찾을 수 있습니다 `fabric-samples`. 이 폴더에는 예제로 제공되고 자습서에서 패브릭 기능을 강조 표시하는 데 사용되는 샘플 체인 코드가 있습니다.

애프터 **fabcar의** chaincode 정의가 채널에 최선을 다하고있다, 스크립트는 호출하여 chaincode을 초기화 `init`기능을하고 장부에 자동차의 초기 목록을 넣어 chaincode를 호출합니다. 그런 다음 스크립트는 체인 코드를 쿼리하여 데이터가 추가되었는지 확인합니다. 체인 코드가 설치, 배포 및 호출 된 경우 로그에 다음과 같은 자동차 목록이 인쇄되어 있습니다.

```
[{"Key":"CAR0", "Record":{"make":"Toyota","model":"Prius","colour":"blue","owner":"Tomoko"}},
{"Key":"CAR1", "Record":{"make":"Ford","model":"Mustang","colour":"red","owner":"Brad"}},
{"Key":"CAR2", "Record":{"make":"Hyundai","model":"Tucson","colour":"green","owner":"Jin Soo"}},
{"Key":"CAR3", "Record":{"make":"Volkswagen","model":"Passat","colour":"yellow","owner":"Max"}},
{"Key":"CAR4", "Record":{"make":"Tesla","model":"S","colour":"black","owner":"Adriana"}},
{"Key":"CAR5", "Record":{"make":"Peugeot","model":"205","colour":"purple","owner":"Michel"}},
{"Key":"CAR6", "Record":{"make":"Chery","model":"S22L","colour":"white","owner":"Aarav"}},
{"Key":"CAR7", "Record":{"make":"Fiat","model":"Punto","colour":"violet","owner":"Pari"}},
{"Key":"CAR8", "Record":{"make":"Tata","model":"Nano","colour":"indigo","owner":"Valeria"}},
{"Key":"CAR9", "Record":{"make":"Holden","model":"Barina","colour":"brown","owner":"Shotaro"}}]
===================== Query successful on peer0.org1 on channel 'mychannel' =====================
```



## 네트워크와 상호 작용

테스트 네트워크를 불러 온 후 `peer`CLI를 사용하여 네트워크와 상호 작용할 수 있습니다. `peer`CLI는 배포 스마트 계약, 업데이트 채널을 호출하거나, 설치 및 CLI에서 새로운 스마트 계약을 배포 할 수 있습니다.

`test-network`디렉토리 에서 작동하는지 확인하십시오 . [샘플, 바이너리 및 Docker 이미지 설치](https://hyperledger-fabric.readthedocs.io/en/release-2.0/install.html) 지시 사항을 따른 경우 저장소 `peer`의 `bin`폴더 에서 바이너리를 찾을 수 있습니다 `fabric-samples`. 다음 명령을 사용하여 해당 바이너리를 CLI 경로에 추가하십시오.

```
export PATH=${PWD}/../bin:${PWD}:$PATH
```

또한 저장소 `FABRIC_CFG_PATH`의 `core.yaml`파일 을 가리 키 도록 설정해야 `fabric-samples`합니다.

```
export FABRIC_CFG_PATH=$PWD/../config/
```

이제 `peer` CLI를 Org1 로 작동 할 수있는 환경 변수를 설정할 수 있습니다 .

```
# Environment variables for Org1

export CORE_PEER_TLS_ENABLED=true
export CORE_PEER_LOCALMSPID="Org1MSP"
export CORE_PEER_TLS_ROOTCERT_FILE=${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=${PWD}/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
export CORE_PEER_ADDRESS=localhost:7051
```

`CORE_PEER_TLS_ROOTCERT_FILE`및 `CORE_PEER_MSPCONFIGPATH`환경 변수는에 Org1의 암호화 소재를 가리 `organizations`폴더에 있습니다.

당신이 사용하는 경우 설치하고 fabcar의 chaincode을 시작, 당신은 지금 당신의 CLI에서 장부를 조회 할 수 있습니다. 채널 원장에 추가 된 자동차 목록을 보려면 다음 명령을 실행하십시오.`./network.sh deployCC`

```
peer chaincode query -C mychannel -n fabcar -c '{"Args":["queryAllCars"]}'
```

명령이 성공하면 스크립트를 실행할 때 로그에 인쇄 된 것과 동일한 자동차 목록이 표시됩니다.

```
[{"Key":"CAR0", "Record":{"make":"Toyota","model":"Prius","colour":"blue","owner":"Tomoko"}},
{"Key":"CAR1", "Record":{"make":"Ford","model":"Mustang","colour":"red","owner":"Brad"}},
{"Key":"CAR2", "Record":{"make":"Hyundai","model":"Tucson","colour":"green","owner":"Jin Soo"}},
{"Key":"CAR3", "Record":{"make":"Volkswagen","model":"Passat","colour":"yellow","owner":"Max"}},
{"Key":"CAR4", "Record":{"make":"Tesla","model":"S","colour":"black","owner":"Adriana"}},
{"Key":"CAR5", "Record":{"make":"Peugeot","model":"205","colour":"purple","owner":"Michel"}},
{"Key":"CAR6", "Record":{"make":"Chery","model":"S22L","colour":"white","owner":"Aarav"}},
{"Key":"CAR7", "Record":{"make":"Fiat","model":"Punto","colour":"violet","owner":"Pari"}},
{"Key":"CAR8", "Record":{"make":"Tata","model":"Nano","colour":"indigo","owner":"Valeria"}},
{"Key":"CAR9", "Record":{"make":"Holden","model":"Barina","colour":"brown","owner":"Shotaro"}}]
```

네트워크 구성원이 원장의 자산을 이전하거나 변경하려고 할 때 체인 코드가 호출됩니다. fabcar 체인 코드를 호출하여 원장에서 자동차 소유자를 변경하려면 다음 명령을 사용하십시오.

```
peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls true --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem -C mychannel -n fabcar --peerAddresses localhost:7051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses localhost:9051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt -c '{"function":"changeCarOwner","Args":["CAR9","Dave"]}'
```

명령이 성공하면 다음 응답이 표시됩니다.

```
2019-12-04 17:38:21.048 EST [chaincodeCmd] chaincodeInvokeOrQuery -> INFO 001 Chaincode invoke successful. result: status:200
```

**참고 :** Java 체인 코드를 배치 한 경우 대신 다음 인수를 사용하여 invoke 명령을 실행하십시오. `'{"function":"changeCarOwner","Args":["CAR009","Dave"]}'` Java로 작성된 Fabcar 체인 코드는 Javascipt 또는 Go로 작성된 체인 코드와 다른 색인을 사용합니다.

fabcar의 chaincode에 대한 보증 정책이 Org1 및 Org2에 의해 서명되는 트랜잭션을 필요로하기 때문에, 명령 요구 호출하는 chaincode 모두를 대상으로 `peer0.org1.example.com`하고 `peer0.org2.example.com`사용하여 `--peerAddresses` 플래그. 네트워크에 대해 TLS가 활성화되어 있으므로 명령은 `--tlsRootCertFiles`플래그를 사용하여 각 피어에 대한 TLS 인증서를 참조해야합니다 .

체인 코드를 호출 한 후 다른 쿼리를 사용하여 호출이 블록 체인 원장의 자산을 어떻게 변경했는지 확인할 수 있습니다. 이미 Org1 피어를 쿼리 했으므로이 기회를 통해 Org2 피어에서 실행되는 체인 코드를 쿼리 할 수 있습니다. 다음 환경 변수를 Org2로 작동하도록 설정하십시오.

```
# Environment variables for Org2

export CORE_PEER_TLS_ENABLED=true
export CORE_PEER_LOCALMSPID="Org2MSP"
export CORE_PEER_TLS_ROOTCERT_FILE=${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=${PWD}/organizations/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp
export CORE_PEER_ADDRESS=localhost:9051
```

이제 다음에서 실행되는 fabcar 체인 코드를 쿼리 할 수 있습니다 `peer0.org2.example.com`.

```
peer chaincode query -C mychannel -n fabcar -c '{"Args":["queryCar","CAR9"]}'
```

결과는 `"CAR9"`Dave에게 전송 되었음을 보여줍니다 .

```
{"make":"Holden","model":"Barina","colour":"brown","owner":"Dave"}
```



## 네트워크 중단

테스트 네트워크 사용을 마치면 다음 명령을 사용하여 네트워크를 종료 할 수 있습니다.

```
./network.sh down
```

이 명령은 노드 및 체인 코드 컨테이너를 중지 및 제거하고 조직 암호 자료를 삭제하며 Docker Registry에서 체인 코드 이미지를 제거합니다. 이 명령은 또한 이전 실행에서 채널 아티팩트 및 도커 볼륨을 제거하므로 문제가 발생한 경우 다시 실행할 수 있습니다.`./network.sh up`



## 다음 단계

테스트 네트워크를 사용하여 로컬 머신에 Hyperledger Fabric을 배치 했으므로 학습서를 사용하여 고유 한 솔루션 개발을 시작할 수 있습니다.

- [스마트 계약을 채널에 배포](https://hyperledger-fabric.readthedocs.io/en/release-2.0/deploy_chaincode.html) 자습서 [를](https://hyperledger-fabric.readthedocs.io/en/release-2.0/deploy_chaincode.html) 사용하여 자체 스마트 계약을 테스트 네트워크에 배포하는 방법에 대해 알아 봅니다 .
- [첫 번째 애플리케이션 작성](https://hyperledger-fabric.readthedocs.io/en/release-2.0/write_first_app.html) 학습서를 방문하여 Fabric SDK에서 제공하는 API를 사용하여 클라이언트 애플리케이션에서 스마트 계약을 호출하는 방법을 학습하십시오.
- 네트워크에보다 복잡한 스마트 계약을 배포 할 준비가 되었다면 [상용 용지 자습서](https://hyperledger-fabric.readthedocs.io/en/release-2.0/tutorial/commercial_paper.html) 를 따라 두 조직이 블록 체인 네트워크를 사용하여 상용 용지를 거래하는 유스 케이스를 탐색하십시오.

[학습서](https://hyperledger-fabric.readthedocs.io/en/release-2.0/tutorials.html) 페이지 에서 패브릭 학습서의 전체 목록을 찾을 수 있습니다 .



## 인증 기관과의 네트워크 구축

Hyperledger Fabric은 PKI (공개 키 인프라)를 사용하여 모든 네트워크 참가자의 작업을 확인합니다. 트랜잭션을 제출하는 모든 노드, 네트워크 관리자 및 사용자는 ID를 확인하기 위해 공개 인증서 및 개인 키가 있어야합니다. 이러한 ID에는 유효한 신뢰 루트가 있어야 네트워크의 구성원 인 조직에서 인증서를 발급 할 수 있습니다. 이 `network.sh`스크립트는 피어 및 주문 노드를 만들기 전에 네트워크를 배포하고 운영하는 데 필요한 모든 암호화 자료를 만듭니다.

기본적으로 스크립트는 암호화 도구를 사용하여 인증서와 키를 만듭니다. 이 도구는 개발 및 테스트 용으로 제공되며 유효한 신뢰 기반을 가진 패브릭 조직에 필요한 암호화 자료를 신속하게 작성할 수 있습니다. 를 실행하면 crypt1 도구가 Org1, Org2 및 Orderer Org에 대한 인증서 및 키를 작성하는 것을 볼 수 있습니다.`./network.sh up`

```
creating Org1, Org2, and ordering service organization with crypto from 'cryptogen'

/Usr/fabric-samples/test-network/../bin/cryptogen

##########################################################
##### Generate certificates using cryptogen tool #########
##########################################################

##########################################################
############ Create Org1 Identities ######################
##########################################################
+ cryptogen generate --config=./organizations/cryptogen/crypto-config-org1.yaml --output=organizations
org1.example.com
+ res=0
+ set +x
##########################################################
############ Create Org2 Identities ######################
##########################################################
+ cryptogen generate --config=./organizations/cryptogen/crypto-config-org2.yaml --output=organizations
org2.example.com
+ res=0
+ set +x
##########################################################
############ Create Orderer Org Identities ###############
##########################################################
+ cryptogen generate --config=./organizations/cryptogen/crypto-config-orderer.yaml --output=organizations
+ res=0
+ set +x
```

그러나 테스트 네트워크 스크립트는 인증 기관 (CA)을 사용하여 네트워크를 시작하는 옵션도 제공합니다. 프로덕션 네트워크에서 각 조직은 조직에 속한 ID를 만드는 CA (또는 여러 중간 CA)를 운영합니다. 조직이 운영하는 CA가 생성 한 모든 ID는 동일한 신뢰 루트를 공유합니다. cryptogen을 사용하는 것보다 시간이 오래 걸리지 만 CA를 사용하여 테스트 네트워크를 가져 오면 프로덕션 환경에서 네트워크를 배포하는 방법을 소개합니다. CA를 배포하면 Fabric SDK를 사용하여 클라이언트 ID를 등록하고 응용 프로그램의 인증서 및 개인 키를 만들 수 있습니다.

Fabric CA를 사용하여 네트워크를 시작하려면 먼저 다음 명령을 실행하여 실행중인 네트워크를 모두 종료하십시오.

```
./network.sh down
```

그런 다음 CA 플래그를 사용하여 네트워크를 불러올 수 있습니다.

```
./network.sh up -ca
```

명령을 실행하면 스크립트가 네트워크의 각 조직마다 하나씩 세 개의 CA를 가져 오는 것을 볼 수 있습니다.

```
##########################################################
##### Generate certificates using Fabric CA's ############
##########################################################
Creating network "net_default" with the default driver
Creating ca_org2    ... done
Creating ca_org1    ... done
Creating ca_orderer ... done
```

`./network.sh` CA가 배포 된 후 스크립트에 의해 생성 된 로그를 검사하는 데 시간이 걸립니다 . 테스트 네트워크는 Fabric CA 클라이언트를 사용하여 각 조직의 CA에 노드 및 사용자 ID를 등록합니다. 그런 다음 스크립트는 enroll 명령을 사용하여 각 ID에 대한 MSP 폴더를 생성합니다. MSP 폴더에는 각 ID에 대한 인증서와 개인 키가 포함되어 있으며 CA를 운영 한 조직에서 ID의 역할과 구성원을 설정합니다. 다음 명령을 사용하여 Org1 관리자의 MSP 폴더를 검사 할 수 있습니다.

```
tree organizations/peerOrganizations/org1.example.com/users/Admin/@org1.example.com/
```

이 명령은 MSP 폴더 구조 및 구성 파일을 나타냅니다.

```
organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/
└── msp
    ├── IssuerPublicKey
    ├── IssuerRevocationPublicKey
    ├── cacerts
    │   └── localhost-7054-ca-org1.pem
    ├── config.yaml
    ├── keystore
    │   └── 58e81e6f1ee8930df46841bf88c22a08ae53c1332319854608539ee78ed2fd65_sk
    ├── signcerts
    │   └── cert.pem
    └── user
```

`signcerts`폴더 에서 관리자의 인증서를 찾을 수 있고 폴더에서 개인 키를 찾을 수 있습니다 `keystore`. MSP에 대한 자세한 내용은 [Membership Service Provider](https://hyperledger-fabric.readthedocs.io/en/release-2.0/membership/membership.html) 개념 주제를 참조하십시오 .

cryptogen과 Fabric CA는 `organizations`폴더의 각 조직에 대한 암호화 자료를 생성 합니다. 디렉토리 의 `registerEnroll.sh`스크립트에서 네트워크를 설정하는 데 사용되는 명령을 찾을 수 있습니다 `organizations/fabric-ca`. Fabric CA를 사용하여 Fabric 네트워크를 배치하는 방법에 대한 자세한 내용은 [Fabric CA 운영 안내서를 참조하십시오](https://hyperledger-fabric-ca.readthedocs.io/en/latest/operations_guide.html) . [ID](https://hyperledger-fabric.readthedocs.io/en/release-2.0/identity/identity.html) 및 [멤버쉽](https://hyperledger-fabric.readthedocs.io/en/release-2.0/membership/membership.html) 개념 주제를 방문하여 Fabric이 PKI를 사용하는 방법에 대해 자세히 알아볼 수 있습니다 .



## 무대 뒤에서 무슨 일이 일어나고 있습니까?

샘플 네트워크에 대한 자세한 내용을 보려면 `test-network`디렉토리 의 파일 및 스크립트를 조사하십시오 . 아래 단계는의 명령을 실행할 때 발생하는 상황을 안내 합니다.`./network.sh up`

- `./network.sh`두 피어 조직과 주문자 조직에 대한 인증서와 키를 작성합니다. 기본적으로 스크립트는 `organizations/cryptogen`폴더 에있는 구성 파일을 사용하여 암호화 도구를 사용 합니다. 당신이 사용하는 경우 `-ca`인증 기관을 만들 플래그를, 스크립트는 직물 CA 서버 구성 파일 및 사용 `registerEnroll.sh`에있는 스크립트 `organizations/fabric-ca`폴더에 있습니다. cryptogen과 Fabric CA는 모두 폴더의 세 조직 모두에 대한 crypto material 및 MSP 폴더를 만듭니다 `organizations`.
- 스크립트는 configtxgen 도구를 사용하여 시스템 채널 생성 블록을 만듭니다. Configtxgen은 파일 `TwoOrgsOrdererGenesis` 에서 채널 프로파일 `configtx/configtx.yaml`을 사용하여 생성 블록을 만듭니다. 블록은 `system-genesis-block`폴더에 저장됩니다 .
- 조직 암호 자료와 시스템 채널 생성 블록이 생성되면 `network.sh`netwowrk의 노드를 불러올 수 있습니다. 스크립트는 폴더 의 `docker-compose-test-net.yaml`파일 `docker`을 사용하여 피어 및 주문자 노드를 만듭니다. 이 `docker`폴더에는 `docker-compose-e2e.yaml`3 개의 Fabric CA와 함께 네트워크 노드를 표시하는 파일 도 포함되어 있습니다 . 이 파일은 Fabric SDK에서 엔드 투 엔드 테스트를 실행하는 데 사용됩니다. 이러한 테스트 실행에 대한 자세한 내용 은 [Node SDK](https://github.com/hyperledger/fabric-sdk-node) 리포지토리를 참조하십시오.
- `createChannel`부속 명령 을 사용하는 경우 폴더 `./network.sh`에서 `createChannel.sh`스크립트를 실행 `scripts`하여 제공된 채널 이름을 사용하여 채널을 작성하십시오. 이 스크립트는 `configtx.yaml`파일을 사용하여 채널 생성 트랜잭션과 2 개의 앵커 피어 업데이트 트랜잭션을 생성합니다. 이 스크립트는 피어 cli를 사용하여 채널을 작성하고 채널에 참여 `peer0.org1.example.com`하고 `peer0.org2.example.com`채널에 연결하고 두 피어를 앵커 피어로 만듭니다.
- 당신이 실행하면 `deployCC`명령을 `./network.sh`런들 `deployCC.sh` 설치하는 스크립트 **fabcar의** 채널에 다음 chaincode를 정의 다음 두 동료에 chaincode을하고 있습니다. 체인 코드 정의가 채널에 커밋되면 피어 cli는를 사용하여 chainocde를 초기화하고 체인 코드를 `Init`호출하여 원장에 초기 데이터를 넣습니다.



## 문제 해결

학습서에 문제점이있는 경우 다음을 검토하십시오.

- 항상 네트워크를 새로 시작해야합니다. 다음 명령을 사용하여 이전 실행에서 아티팩트, 암호화 자료, 컨테이너, 볼륨 및 체인 코드 이미지를 제거 할 수 있습니다.

  ```
  ./network.sh down
  ```

  당신은 **것입니다** 당신이 오래된 용기, 이미지, 볼륨을 제거하지 않으면 오류를 참조하십시오.

- Docker 오류가 표시되면 먼저 Docker 버전 ( [전제 조건](https://hyperledger-fabric.readthedocs.io/en/release-2.0/prereqs.html) )을 확인한 후 Docker 프로세스를 다시 시작하십시오. Docker의 문제는 종종 즉시 인식되지 않습니다. 예를 들어, 노드가 컨테이너 내에 마운트 된 암호화 자료에 액세스 할 수 없기 때문에 발생하는 오류가 표시 될 수 있습니다.

  문제가 지속되면 이미지를 제거하고 처음부터 시작할 수 있습니다.

  ```
  docker rm -f $(docker ps -aq)
  docker rmi -f $(docker images -q)
  ```

- 작성, 승인, 커미트, 호출 또는 조회 명령에 오류가 표시되면 채널 이름 및 체인 코드 이름을 올바르게 업데이트했는지 확인하십시오. 제공된 샘플 명령에는 자리 표시 자 값이 있습니다.

- 아래 오류가 표시되면

  ```
  Error: Error endorsing chaincode: rpc error: code = 2 desc = Error installing chaincode code mycc:1.0(chaincode /var/hyperledger/production/chaincodes/mycc.1.0 exits)
  ```

  이전 실행의 체인 코드 이미지 (예 : `dev-peer1.org2.example.com-fabcar-1.0`또는 `dev-peer0.org1.example.com-fabcar-1.0`)가있을 수 있습니다. 그것들을 제거하고 다시 시도하십시오.

  ```
  docker rmi -f $(docker images | grep peer[0-9]-peer[0-9] | awk '{print $3}')
  ```

- 아래 오류가 표시되면

  ```
  [configtx/tool/localconfig] Load -> CRIT 002 Error reading configuration: Unsupported Config Type ""
  panic: Error reading configuration: Unsupported Config Type ""
  ```

  그런 다음 `FABRIC_CFG_PATH`환경 변수를 올바르게 설정하지 않았습니다 . configtxgen 도구는 configtx.yaml을 찾으려면이 변수가 필요합니다. 돌아가서를 실행 한 다음 채널 아티팩트를 다시 작성하십시오.`export FABRIC_CFG_PATH=$PWD/configtx/configtx.yaml`

- 여전히 "활성 엔드 포인트"가 있다는 오류가 표시되면 Docker 네트워크를 정리하십시오. 이렇게하면 이전 네트워크가 지워지고 새로운 환경에서 시작할 수 있습니다.

  ```
  docker network prune
  ```

  다음과 같은 메시지가 나타납니다.

  ```
  WARNING! This will remove all networks not used by at least one container.
  Are you sure you want to continue? [y/N]
  ```

  를 선택하십시오 `y`.

- 다음과 유사한 오류가 표시되는 경우

  ```
  /bin/bash: ./scripts/createChannel.sh: /bin/bash^M: bad interpreter: No such file or directory
  ```

  문제의 파일 ( 이 예제에서는 **createChannel.sh** )이 Unix 형식으로 인코딩되어 있는지 확인하십시오 . 이것은 대부분 설정하지 않음으로써 발생 된 `core.autocrlf`에 `false`당신의 망할 놈의 구성 (참조 [윈도우 엑스트라](https://hyperledger-fabric.readthedocs.io/en/release-2.0/prereqs.html#windows-extras) ). 이 문제를 해결하는 방법에는 여러 가지가 있습니다. 예를 들어 vim 편집기에 액세스 할 수 있으면 파일을여십시오.

  ```
  vim ./fabric-samples/test-network/scripts/createChannel.sh
  ```

  그런 다음 다음 vim 명령을 실행하여 형식을 변경하십시오.

  ```
  :set ff=unix
  ```

- 주문할 때 주문자가 종료되거나 주문 서비스에 연결할 수 없어 채널 작성 명령이 실패한 경우 명령을 사용 하여 주문 노드에서 로그를 읽으십시오. 다음과 같은 메시지가 나타날 수 있습니다.`docker logs`

  ```
  PANI 007 [channel system-channel] config requires unsupported orderer capabilities: Orderer capability V2_0 is required but not supported: Orderer capability V2_0 is required but not supported
  ```

  Fabric 버전 1.4.x 도커 이미지를 사용하여 네트워크를 실행하려고 할 때 발생합니다. 테스트 네트워크는 Fabric 버전 2.x를 사용하여 실행해야합니다.
