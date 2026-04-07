import abc


class BaseLayer(abc.ABC):
    @abc.abstractmethod
    def compile():
        """
        Applies the compilation associated with this layer to the current IR of the circuit,
        returning the circuit (possibly in a different IR).
        """

    @classmethod
    @abc.abstractmethod
    def set_compile_args():
        """
        Sets arguments for the self.compile() function according to a passed flag dictionary.
        """

    @classmethod
    @abc.abstractmethod
    def compilation_flags():
        """
        Used for getting the compilation flags associated with a certain compilation layer.
        """
