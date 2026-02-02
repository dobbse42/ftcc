import abc


class BaseLayer(abc.ABC):
    @abc.abstractmethod
    def compile():
        """
        Applies the compilation associated with this layer to the current IR of the circuit,
        returning the circuit (possibly in a different IR).
        """
