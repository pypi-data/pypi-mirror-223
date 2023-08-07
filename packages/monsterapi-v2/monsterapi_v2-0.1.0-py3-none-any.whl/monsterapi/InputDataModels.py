from pydantic import BaseModel, Field
from typing import Optional, Literal, Union, List, Dict


class LLMInputModel1(BaseModel):
    """
    Supports Following models: Falcon-40B-instruct, Falcon-7B-instruct, openllama-13b-base, llama2-7b-chat

    prompt	string	Prompt is a textual instruction for the model to produce an output.	Required
    top_k	integer	Top-k sampling helps improve quality by removing the tail and making it less likely to go off topic.	Optional
    (Default: 40)
    top_p	float	Top-p sampling helps generate more diverse and creative text by considering a broader range of tokens.	Optional
    (Default: 1.0)
    temp	float	The temperature influences the randomness of the next token predictions.	Optional
    (Default: 0.98)
    max_length	integer	The maximum length of the generated text.	Optional
    (Default: 256)
    repetition_penalty	float	The model uses this penalty to discourage the repetition of tokens in the output.	Optional
    (Default: 1.2)
    beam_size	integer	The beam size for beam search. A larger beam size results in better quality output, but slower generation times.	Optional
    (Default: 1)    
    """
    prompt: str
    top_k: int = 40
    top_p: float = Field(0.9, ge=0., le=1.)
    temp: float = Field(0.98, ge=0., le=1.)
    max_length: int = 256
    repetition_penalty: float = 1.2
    beam_size: int = 1


class LLMInputModel2(BaseModel):
    """
    Supports Following models: MPT-30B-instruct, MPT-7B-instruct

    prompt:	string	Instruction is a textual command for the model to produce an output.	Required
    top_k	integer	Top-k sampling helps improve quality by removing the tail and making it less likely to go off topic.	Optional
    (Default: 40)
    top_p	float	Top-p sampling helps generate more diverse and creative text by considering a broader range of tokens.	Optional
    Allowed Range: 0 - 1
    (Default: 1.0)
    temp	float	Temperature is a parameter that controls the randomness of the model's output. The higher the temperature, the more random the output.	Optional
    (Default: 0.98)
    max_length	integer	Maximum length of the generated output.	Optional
    (Default: 256)
    """
    prompt: str
    top_k: int = 40
    top_p: float = Field(0.9, ge=0., le=1.)
    temp: float = Field(0.98, ge=0., le=1.)
    max_length: int = 256

class SDInputModel(BaseModel):
    """
    Support following models: text2img, text2img-sdxl

    prompt:	string	Your input text prompt	Required
    negprompt:	string	Negative text prompt	Optional
    samples:	integer	No. of images to be generated. Allowed range: 1-4	Optional
    (Default: 1)
    steps:	integer	Sampling steps per image. Allowed range 30-500	Optional
    (Default: 30)
    aspect_ratio: string.  Allowed values: square, landscape, portrait	Optional
    (Default: square)
    guidance_scale:	float.	Prompt guidance scale	Optional
    (Default: 7.5)
    seed:	integer	Random number used to initialize the image generation.	Optional
    (Default: random)
    """
    prompt: str
    negprompt: Optional[str] = ""
    samples: Optional[int] = Field(1, ge=1, le=4)
    steps: Optional[int] = Field(30, ge=30, le=500)
    aspect_ratio: Optional[Literal['square', 'landscape', 'portrait']] = 'square'
    guidance_scale: Optional[float] = 7.5
    seed: Optional[int] = None


MODELS_TO_DATAMODEL = {
            'falcon-7b-instruct': LLMInputModel1,
            'falcon-40b-instruct': LLMInputModel1,
            'mpt-30B-instruct': LLMInputModel2,
            'mpt-7b-instruct': LLMInputModel2,
            'openllama-13b-base': LLMInputModel1,
            'llama2-7b-chat': LLMInputModel1,
            "sdxl-base": SDInputModel,
            "txt2img": SDInputModel
        }