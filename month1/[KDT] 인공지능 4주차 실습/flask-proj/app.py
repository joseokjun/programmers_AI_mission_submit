# jsonify는 파이썬에서 사용하는 dict형식을 자바스크립트에서 사용하는 데이터 저장방식 으로 바꿔주고
# request는 http request를 다룰수 있는 모듈이다.
from flask import Flask, jsonify, request

# Flask를 바탕으로한 객체를 생성한다.
# 인자로 __name__을 전달한다. 이것은 Flask의 name을 app으로 넣어준다는 의미이다.
app = Flask(__name__)

# @는 파이썬 데코레이터를 의미한다. '/'이 주소가 등장했을때, 이 주소를 요청받았을때 
# 밑에있는 함수를 실행하라는 의미로 받아들일수 있다.

menus = [{"id":1, "name":"Esspresso", "price":3000},
         {"id":2, "name":"Americano", "price":4100},
         {"id":3, "name":"CafeLatte", "price":4600}
         ]
@app.route('/') # root의 자료를 접근하는 주소 
def hello_flask():
    return "Hello World"

# GET, POST 라는 2가지 메서드를 이용해서 같은 자원에 대해서 다른 로직을 구현해 보자

# GET /menus GET의 경우 자료를 가지고 올 때 사용한다.
@app.route('/menus') # menus라는 자원을 접근
def get_menus():

    # menus는 리스트 타입이라 리스트 타입은 json으로 변환이 안되기 때문에 menus를 value로 하는 dict 형태로 만든후
    # jsonify를 적용하여 json화 시켜서 json형태로 변환될 수있게 한다.
    return jsonify({"menus": menus}) # 리턴되는 값은 실제로 json형태가 된다.


# POST /menus POST의 경우 자료를 자원에 추가하는 역할을 수행
'''
app.route는 기본적으로 methods라고 하는 인자가 존재한다. default값으로 이 인자가 GET으로 되어있다.
@app.route('/menus, methods=['GET'])
그래서 우리는 위에 GET의 경우에 따로 methods를 명시하지 않은것이다. 실제로 가장 많이 사용되는 http method가 get이다.
그래서 보통 생략한다. 하지만 이를 제외한 나머지 http동사들, PUT,FETCH,POST등과 같은 메소드들은
특수한 경우이기 때문에 명시를 반드시 해줘야한다. 이 인자를 리스트의 형태로 담아주게 된다.'''
@app.route('/menus', methods=['POST'])
def create_menu(): # request가 JSON이라고 가정
    # 전달받은 자료를 menus 자원에 추가
    # 이때 사용자가 주는 데이터의 형식을 json이라고 가정 
    request_data = request.get_json() # 이 json의 형태는 {"name": ... "price": ...이라고 가정}
    '''flask에서 import 했던 requests의 경우 자동적으로 클라이언트가 서버로부터 post를 이용
    해서 요청할때 담기는 자료가 담겨있다. 그래서 이를 get_json을 이용해서 파싱한후 request_data
    라는 변수에 담게 된다. 이 상황에서 request_data의 경우 파이썬이 알아볼 수있는 data형인
    dict 형태가 되게 된다. json과 dict의 경우 완전히 같은 데이터타입은 아니기 때문에 .get_json
    이라는 변환과정을 거쳐야한다. POST에서 딸려오는 데이터를 payload라고도 한다.'''
    new_menu = {
        "id" : 4,
        "name" : request_data['name'],
        "price": request_data['price'],
    }
    menus.append(new_menu)
    return jsonify(new_menu)

# 보너스 과제: POST 메서드 수정하기
'''
새로운 menu를 추가하는 POST 영역에서 id가 4로 고정되어있는 문제가 발생합니다.
POST 요청이 들어올 때마다 id가 하나씩 증가하여 menu 리스트에 추가될 수 있도록 코드를 수정해주세요.
이 과제는 필수 과제 이후에 진행되어야 합니다.
'''
'''
def create_menus():
    request_data = request.get_json() 

    new_menu = {
        "id": len(menus)+1,
        "name": request_data['name'],
        "price": request_data['price'],
    }

    menus.append(new_menu)
    return jsonify(new_menu)
'''

# 이렇게 같은 end point인 /menus에 대해서 각각 다른처리(동사) GET, POST를 이용해서 위와같이
# 상황에 맞는 로직을 구현할 수있다.
# 이제 이 2가지 API를 테스트 해보도록 하자

### 과제 
# PUT /menus   | 해당 자료를 수정한다.
@app.route('/menus/<int:id>', methods=['PUT'])
def update_menus(id):
    update_data = request.get_json()
    try:
        menus[id-1]["name"] = update_data["name"]
        menus[id-1]["price"] = update_data['price']
        return jsonify(menus[id-1])
    except Exception as e:
        print(e)
        return jsonify({'error': "해당 자료가 존재하지 않습니다."})


# DELETE /menus   | 해당 자료를 삭제한다.
@app.route('/menus/<int:id>', methods=['DELETE'])
def delete_menus(id):
    try:
        del menus[id-1]
        return jsonify(menus)
    except Exception as e:
        print(e)
        return jsonify({'error': "해당 자료가 존재하지 않습니다."})

# 이것은 __name__(스페이스)가 main인 경우, 즉 내가 app.py를 직접적으로 실행한 경우를 말한다.
# 그런 경우에는 앱을 실행하라는 의미이다.
if __name__ == '__main__':
    app.run()