import os
from pathlib import Path
from uuid import UUID
from uuid import uuid4

from app_manager import AppManager, AppStructure, ModelInfo
from maker_manager import MakerManager
from maker_manager.thread_handler import ConvertThreadHandler


class ConvertService:
    """기존 앱을 바탕으로 새로운 앱을 생성

    기존 앱에서 모델을 교체해 새로운 앱을 생성한다.

    실행 순서:
        1. is_local_maker_installed: waffle maker가 local에 설치되어 있는지 확인한다.
        2. get_model_info: 입력한 App의 모델 정보를 받아온다.
        3. add_convert_info: 모델 정보를 바탕으로 변경할 모델들을 입력한다.
        4. convert_models: 입력한 모델을 변환하고 기존 App에서 교체한다.
        5. package_app: 새로운 앱으로 패키징한다.

    Attributes:
        workspace (Path): 작업할 경로, 일반적으로 ~/.waffle_box
        origin_app_path (Path): 사용자가 입력한 기존 App 경로
        final_app_path (Path): 새로운 App을 저장할 경로
        img_tag (str): trt 변환을 위한 컨테이너 태그명
        convert_list (dict[UUID, Path]): 변경할 모델 리스트
        app_manager (AppManager): app manager
        maker_manager (MakerManager): maker manager

    """

    def __init__(
        self, workspace: Path, input: Path, output: Path, dx_target_version: str, gpu_num: int
    ) -> None:
        """
        Args:
            workspace (Path): 작업할 경로
            input (Path): 변환할 App 경로
            output (Path): 새로운 App을 저장할 경로
            dx_target_version (str): 변환할 App의 target Autocare-D 버전
            gpu_num (int): 작업할 GPU 번호

        Raises:
            AppParsingError
            DockerError

        """
        self.workspace: Path = workspace
        self.origin_app_path: Path = input
        self.final_app_path: Path = output

        # TODO: make image tag converter
        self.img_tag = "snuailab/trt:8.5.2.2"

        self.convert_list: dict[UUID, Path] = {}

        self.app_manager = AppManager(self.workspace, self.origin_app_path)
        self.maker_manager = MakerManager(self.img_tag, gpu_num=gpu_num, workspace=self.workspace)

    def is_local_maker_installed(self) -> bool:
        """Waffle maker가 local에 설치되어 있는가?

        Returns:
            True: 이미지가 설치되어 있음
            False: 이미지가 설치되어 있지 않음
        """
        return self.maker_manager.check_image_exist_at_local()

    def get_model_info(self) -> list[ModelInfo]:
        """모델 정보 받아오기

        사용자가 입력한 App의 모델 정보들을 리스트로 반환한다.

        Returns:
            list[ModelInfo]: 모델 정보 리스트

        """
        return self.app_manager.app_structure.models

    def add_convert_info(self, model_id: UUID, new_model_path: Path) -> None:
        """변환할 모델 정보 등록

        변환할 모델 정보를 등록한다. App의 모델 id와 새로운 모델 경로를 등록한다.
        등록할 만큼 호출한다.

        Args:
            model_id (UUID): 교체할 모델의 UUID
            new_model_path (Path): 새로운 모델 파일 경로

        """
        self.convert_list[model_id] = new_model_path

    def convert_models(self, print_output: bool, using_thread: bool = False,
                        allow_multiple_containers: bool = False,
                        thread_handler: ConvertThreadHandler = None) -> ConvertThreadHandler:
        """모델 변화

        사용자가 등록한 모델들을 변환한다.

        Args:
            print_output (bool): 변환 과정을 출력 여부

        Raises:
            AppManager
            MakerManager

        """
        replace_remove_data = []

        for id, file_path in self.convert_list.items():
            model_info = self.app_manager.find_model_info_by_id(id)

            if not model_info:
                return

            onnx_config = model_info.to_onnx_config()

            engine_file_path = self.workspace.joinpath(f"{uuid4()}_{model_info.engine_file_name}")

            thread_handler = self.maker_manager.convert_onnx_to_engine_at_local(
                input=file_path,
                output=engine_file_path,
                convert_config=onnx_config,
                print_output=print_output,
                using_thread=using_thread,
                allow_multiple_containers=allow_multiple_containers,
                thread_handler=thread_handler
            )

            replace_remove_data.append([id, engine_file_path])

        return thread_handler, replace_remove_data

    def package_app(self) -> None:
        """새로운 App 생성"""
        self.app_manager.package(self.final_app_path)
