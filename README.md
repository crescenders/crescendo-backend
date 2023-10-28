# Crescendo Backend Repository.

### Python 코딩 컨벤션

- 기본적으로 PEP8 을 따라야 합니다.
- `black` 을 사용하여 코드를 정리합니다.
- `isort` 를 사용하여 import 를 정리합니다.
- `flake8` 을 사용하여 코드 품질을 검사합니다.
- `mypy` 를 사용하여 타입 힌트를 검사합니다. (현재 부분적으로 적용되어 있습니다.)

### View 코딩 컨벤션

- 가급적이면 함수형 뷰보다는, 클래스 기반 뷰를 사용해야 합니다.
- 네이밍은 `APIView` 를 상속받은 클래스는 `<Entity><Action>API` 형태로, `Viewset` 을 상속받은 클래스는 `<Entity>ViewSet` 형태로 작성합니다.
- `GenericAPIView` 를 상속받은 커스텀 `Viewset` 은 모든 action 을 네이밍에 포함시켜야 합니다.
    - 예를 들어, 사용자를 생성하고, 수정하고, 상세 조회할 수 있는 `ViewSet` 은 `UserCreateUpdateRetrieveViewSet` 으로 작성합니다.
- `rest_framework` 의 `generics` 를 적극 활용해야 합니다.
- `APIView` 를 상속받은 클래스 기반 뷰의 클래스 변수들은 아래의 순서를 따라야 합니다.
    1. `queryset`
    2. `serializer_class`
    3. `permission_classes`
    4. `authentication_classes`
    5. `pagination_class`
    6. `filter_backends`
    7. `search_fields`
    8. `ordering_fields`
    9. `ordering`
    10. `lookup_field`
    11. `lookup_url_kwarg`
- `APIView` 를 상속받은 클래스 기반 뷰의 메서드는 아래의 순서로 작성해야 합니다.
    1. get_queryset
    2. get_object
    3. get_serializer_class
    4. get
    5. post
    6. put
    7. patch
    8. delete
- `Viewset` 기반 뷰의 `action` 메서드는 아래의 순서로 작성해야 합니다.
    1. list
    2. create
    3. retrieve
    4. update
    5. partial_update
    6. destroy
