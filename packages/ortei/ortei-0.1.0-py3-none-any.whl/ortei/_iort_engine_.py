import abc
from typing import Any, Dict, List, Tuple

class IORTEngine(metaclass=abc.ABCMeta):
    """
    ## IORTEngine

    Abstract class for onnx runtime engine.
    """
    ort_session:Any
    """
    ## ort_session 
       
    ONNX Runtime Session instance.

        Example ::

        self.ort_session = ort.InferenceSession(
            path_or_bytes=onnx_fp32_path,
            sess_options=self.session_options,
            providers=providers,
            )
    """
    io_shape:Dict[str,List[int]]
    """
    ## io_shape

    This is a dictionary that records dimension information for each io.
        
        Example :: 

        self.io_shape = {
            "input_images": [1, 3, 1080, 1920],
            "output_images":  [1, 3, 1080, 1920],
            }
    """
    io_binding:Any
    """
    ## io_binding

    This is a iobinding instance of ort session.

        Example :: 

        self.io_binding = self.ort_session.io_binding()
    """
    io_data_cpu:Dict[str,Any]
    """
    ## io_data_cpu

    This is a dictionary of io buffers handled in the host memory area.

        Example ::

        self.io_data_cpu = {key:np.zeros(io_shapes[key], np.float32) for key in self.io_shapes}
    """
    io_data_ort:Dict[str,Any]
    """
    ## io_data_ort

    This is a dictionary of io buffers handled in the device memory area.
    
        Example ::

        io_data_cpu = self.io_data_cpu
        device_name = self.device_name
        device_id = self.device_name
        self.io_data_ort = {key:ort.OrtValue.ortvalue_from_numpy(io_data_cpu[key], device_name, device_id) for key in io_data_cpu}
    """
    device_name:str
    """
    ## device_name

    The name of the device interfering with the ort session.
    """
    device_id:int
    """
    ## device_id

    The ID of the device interfering with the ort session.
    """
    input_data:Any
    """
    ## input_data

    The original data to pass to the model.
    """
    output_data:Any
    """
    ## output_data
    
    Result data output by the model.
    """

    def __init__(self, **argv):
        self._init_members(**argv)
        member_check_list = [
            self.ort_session,
            self.io_shape,
            self.io_binding,
            self.io_data_cpu,
            self.io_data_ort,
            self.device_name,
            self.input_data,
            self.output_data,
        ]
        for member_value in member_check_list:
            assert member_value is not None, f"ERROR, {member_value} is None."

    @abc.abstractmethod
    def _init_members(self) -> None:
        """
        ## _init_members

        Create member variables here.

        You should create below member variable in init.

         * self.ort_session
         * self.io_shape
         * self.io_binding
         * self.io_data_cpu
         * self.io_data_ort
         * self.device_name
         * self.input_data
         * self.output_data

        """
        raise NotImplemented

    @abc.abstractmethod
    def _bind_model_io(self) -> None:
        """
        ## _bind_model_io

        You need to perform io_bindings and ort value binding here.
        
        ### Usage::
            
            io_binding = self.io_binding
            
            io_data_ort = self.io_data_ort

            io_binding.bind_ortvalue_input("input_images", io_data_ort["input_images"])
            
            io_binding.bind_ortvalue_output("output_images", io_data_ort["output_images"])

        """
        raise NotImplemented
    
    @abc.abstractmethod
    def set_input_data(self, data:Any) -> None:
        """
        ## set_input_data

        Set input_data.
        """
        raise NotImplemented
    
    @abc.abstractmethod
    def get_output_data(self) -> Any:
        """
        ## get_output_data

        Get output_data.
        """
        raise NotImplemented

    @abc.abstractmethod
    def convert_data2input(self) -> None:
        """
        ## convert_data2input

        Convert the data to the input form of the model (pre-processing).
        """
        raise NotImplemented

    @abc.abstractmethod
    def move_host2device(self) -> None:
        """
        ## move_host2device

        Upload converted input_data to device.
        """
        raise NotImplemented

    @abc.abstractmethod
    def inference(self) -> None:
        """
        ## inference

        The device performs inference.
        """
        raise NotImplemented

    @abc.abstractmethod
    def move_device2host(self) -> None:
        """
        ## move_device2host

        Download the output from the device to the host.
        """
        raise NotImplemented

    @abc.abstractmethod
    def convert_output2data(self) -> None:
        """
        ## convert_output2data

        Convert the output value of the model into the final result form (post-processing).
        """
        raise NotImplemented