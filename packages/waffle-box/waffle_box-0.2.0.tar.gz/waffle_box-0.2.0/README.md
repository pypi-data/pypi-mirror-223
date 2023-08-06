# What is Waffle Box.
Waffle Box는 기존 Autocare App을 Waffle로 만든 모델로 교체해 새로운 App을 생성해 줍니다.

# Build
Waffle Box는 python package 관리자인 Poetry를 기반으로 빌드 및 배포합니다.
Install poetry: https://python-poetry.org/docs/

``` bash
poetry build
```

# Dependency
- python
  - 3.10

# Install
## Install from code
```bash
poetry install
```

## Install from PyPI
```bash
pip install waffle-box
```

# Usage
## CLI
### Pull Waffle Maker Image
```bash
wb --dx-version 1.6.2 pull --login
```

### Convert App
```bash
wb --dx-version 1.6.2 convert safety_app_1.0.0.zip -o safety_app_1.0.1.zip
```

### Convert Model
```bash
wb --dx-version 1.6.2 bake ~/flame.onnx -O ~/model.engine --precision fp32 --batch 16 --shapes 3x640x640
```

## API
### convert_model시 주의사항
Bake와 Convert에 convert_model(s) 메소드가 존재 합니다.
이를 cli가 아닌, api 제공을 위해 사용한다면 다음 인자를 사용하여야 합니다.
```text
using_thread (bool): thread 동작 여부.
allow_multiple_containers (bool): convert를 동시에 가능한지 여부.
```
그리고, convert_model(s)은 thread_handler를 return 합니다.
handler.status를 통해 thread의 상태를 확인할 수 있으며 다음의 상태를 가집니다.
```python
class ThreadStatus(Enum):
    CREATE = 1
    RUN = 2
    TERMINATE = 3
    EXCEPTION = 4
```
thread 옵션을 주면, start하여 CREATE -> RUN 상태가 됩니다.
그리고 작업 종료 후 자동적으로 RUN -> TERMINATE 상태가 되며 에러 발생 시 EXCEPTION 상태가 됩니다.

이를 hander.join()을 통해 TERMINATE나 EXCEPTION 상태에서 thread join이 가능합니다.
### ! allow_multiple_containers 주의사항
App에서 여러개의 model을 변환할 때, container의 생성과 파괴가 반복됩니다.  
파괴하고 생성되기 전에 새로운 App 변환을 시도하면, 기존 App의 컨테이너 생성이 실패하여 에러가 발생할 수 있습니다.  
(docker container의 개수 제한은 있지만, lock이 존재하지 않습니다.)
