<div align="center">
  

  
<a href="https://crescendo-study.site">
 <img src="https://hackmd.io/_uploads/ryeulfix46.png" width="150px" >
</a>

## [Crescendo](https://crescendo-study.site)

    
[서비스 소개](#서비스-소개) | [기술적 세부사항](#-기술적-세부-사항) | [팀원 소개](#팀원-소개)
    
</div>


##  서비스 소개

### 👋 개발자를 위한 소규모 스터디 플랫폼, 크레센도입니다.

**🔊 `Crescendo`, 점점 더 크고 강하게.** 

"크레센도"는 이탈리아어에서 유래한 음악 용어입니다. 이것은 '성장하다' 또는 '증가하다'를 의미합니다. 음악에서는 음량이 점점 증가하는 것을 나타내는 표현으로 사용되는데, 조용한 부분에서 시작하여 점차적으로 강하게, 또는 크게 플레이하라는 의미를 가집니다.
분야를 막론하고, "성장" 이라는 단어는 스스로 발전하고자 하는 이들의 가슴을 두근거리게 합니다. 크레센도 서비스를 통해서, 발전을 원하는 열정적인 사람들과 "성장" 해 보세요. ***점점 더 크고, 강하게!***

**👨‍👩‍👧‍👦 함께 성장하는 즐거움**

크레센도를 통해 개발자들은 자신의 역량을 향상시키고, 다른 개발자들과 소통하며 지식을 공유할 수 있습니다. 또한, 다양한 개발 분야의 스터디에 참여하여 새로운 지식을 습득하고, 자신의 관심 분야를 확장할 수 있습니다. 여러가지 스터디를 즐기며, 열정적인 스터디 멤버들과 함께 성장하는 경험을 만나보세요!

**📈 체계적이고 효율적인 스터디 운영**

크레센도는 개발자들이 자유롭게 스터디를 개설하고 참여할 수 있는 서비스입니다. 운영하고 싶은 스터디를 개설하고 과제를 등록할 수 있으며, 가입하고 싶은 스터디에 참여하여 과제를 제출할 수 있습니다. 팀원을 모집하고 과제를 등록하거나, 원하는 스터디에 참여하여 과제를 제출해보세요!

**📚 쉽고 빠른 스터디 탐색**

개발 카테고리 별로 분류된 스터디를 탐색할 수 있으며, 키워드로 검색이 가능합니다. 가입하고 싶은 스터디를 찾았다면 참여 신청을 보내보세요. 스터디 멤버로 승인되었다면 스터디원으로서 활동할 수 있습니다.


## ⚙ 기술적 세부 사항

### 백엔드
#### 기술 스택
![image](https://hackmd.io/_uploads/rypwMpPE6.png)

- **WAS** 구축을 위해 **Python** 과 **Django & Django REST framework** 를 사용했어요. *"마감 기한이 있는 완벽주의자를 위한 웹 프레임워크"*, **Django** 의 기능들을 적극 활용하는 경험을 할 수 있었어요.
- 인증의 도구로서는 **JWT** 를 활용하였습니다.
- **Oracle** 기반 클라우드 서비스를 적극 활용하는 경험을 했어요.
- 웹 서버로서 **Nginx** 를 활용하여, **WAS** 와 **Web Server** 를 분리할 수 있었어요.
- **Docker & Docker Compose**, **Github Actions** 를 활용해 배포 자동화를 효율적으로 구성할 수 있었어요.

#### CI & CD

- **Oracle Cloud Infrastructure** 서비스를 적극 활용해 배포했어요.
- **DBMS** 서버로 **Oracle Autonomous Database** 를 활용했어요.
- **Github** 저장소의 **main** 브랜치에 병합이 일어나면, **Github Actions** 을 활용하여 아래의 작업을 수행해 배포를 자동화할 수 있었어요.
    1. **Github Actions** 에서 **Docker** 이미지를 빌드합니다.
    2. 빌드한 이미지를 **DockerHub** 에 업로드합니다.
    3. 오라클 컴퓨트 인스턴스 서버에 접속해 만들어진 **Docker** 이미지를 새로 배포합니다.
- **LetsEncrypt** 와 **DuckDNS** 를 활용해 **HTTPS** 를 적용하였습니다.
- 배포 시 아래의 작업을 통해 코드 품질을 유지했어요.
    1. **flake8** 을 통하여 코드의 스타일을 검사합니다.
    2. 만약 **flake8** 검사에 실패하면, 배포는 실패합니다.
    3. 저장소에 작성된 **Django** 테스트 코드를 **Coverage** 와 함께 실행합니다.
    4. 만약 커버리지가 일정 수준 이하이거나 테스트 코드가 실패하면, 배포는 실패합니다.
- 정적 타입 검사 도구, **Mypy** 를 통해 파이썬의 타입 힌트를 일부 적용했어요.
- **pre-commit** 을 활용해 커밋 시 **flake8**, **black** 검사가 통과하는 것을 보장했어요. 이렇게 함으로서, 커밋 시 일정 품질 이상의 코드만 저장소에 병합될 수 있도록 할 수 있었습니다.

#### 고민의 흔적들

- [**[REAL Python – Flask] – “어떻게 Flask 프로젝트를 구성할 것인가?”**](https://www.gdsanadevlog.com/planguages/real-python-flask-%ec%96%b4%eb%96%bb%ea%b2%8c-flask-%ed%94%84%eb%a1%9c%ec%a0%9d%ed%8a%b8%eb%a5%bc-%ea%b5%ac%ec%84%b1%ed%95%a0-%ea%b2%83%ec%9d%b8%ea%b0%80/)
해당 프로젝트의 원래 프레임워크는 **Django** 가 아니라 **Flask** 였어요. 맨 처음, 프로젝트를 셋업할 때 프로젝트를 어떻게 구성해야 할지에 대해서 깊은 고민을 할 수 있었는데, 고민한 과정을 블로그에 정리하였습니다.
- [**[REAL Python – Flask] – “Python에서 궁극의 Repository 구현하기”**](https://www.gdsanadevlog.com/planguages/real-python-flask-python%ec%97%90%ec%84%9c-jparepository-like-repository-%ea%b5%ac%ed%98%84%ed%95%98%ea%b8%b0/)
**Flask** 와 함께, 저만의 **Repository Pattern** 을 어떻게 구현할 수 있었는지를 정리했어요. **Python** 기반 생태계뿐만 아니라, **Repository Pattern** 을 사용하는 다른 생태계는 어떻게 구성되어 있는지 돌아보고 고민할 수 있었습니다.
- **Flask** 와 **Flask-Smorest** 라는 프레임워크를 사용하다 **Django&DRF** 로 기술 스택을 변경하게 된 이유는 **Flask-Smorest** 의 **multipart/form-data** 에 대한 문서화 지원이 부족했기 때문이었어요. 이미 상당 부분 개발이 진행된 프로젝트의 프레임워크를 변경하는 경험을 하며, "기술 스택은 신중하게, 생태계와 레퍼런스가 풍부한 것을 선택할 것" 이라는 교훈을 얻을 수 있었어요.




## 팀원 소개

|     Frontend   |    Frontend    |   Frontend    |    Backend    |
|:-------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------:|:--------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------:|
| <img src="https://avatars.githubusercontent.com/u/87893624?v=4" width="150px"/> | <img src="https://avatars.githubusercontent.com/u/48711263?v=4" width="150px"  /> | <img src="https://avatars.githubusercontent.com/u/51291185?v=4" width="150px" /> | <img src="https://avatars.githubusercontent.com/u/88619089?v=4" width="150px" /> |
| **[이하람](https://github.com/halamlee)**  |  **[김태현](https://github.com/thyeone)**  |  **[김태영](https://github.com/overtae)**  | **[정재균](https://github.com/TGoddessana)**  |
