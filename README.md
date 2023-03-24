## Layer

resources # 클라이언트에게 보여지는 역할을 수행  
(dto)
services # 비즈니스 로직이 위치한 Layer  
(dto)
repositories # ORM 의 데이터 조회에 대한 Interface  
(dto)
models # DB 와 소통, Class <-> Table 1:1 매핑  
(orm)
DB # 실제 데이터베이스 Layer, sqlite, postgresql, oracle and etc..  