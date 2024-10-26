from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
from typing import Optional
from starlette import status

# Import the original documentation generation function
from adhoc.db.database import get_explanations, get_codebase_summary
from adhoc.utils.latex_utils import render_latex_document
from adhoc.utils.markdown_utils import render_markdown_document
from adhoc.utils.word_utils import render_word_document
from adhoc.utils.config_utils import load_config

# Initialize FastAPI app
app = FastAPI(
    title="ADHOC Documentation Generator API",
    description="API for generating documentation from codebase",
    version=1.0)

# Define allowed output formats
class OutputFormat(str, Enum):
    LATEX = "latex"
    MARKDOWN = "markdown"
    WORD = "word"

# Request model
class DocumentationRequest(BaseModel):
    output_format: OutputFormat
    author_name: Optional[str] = "Default Author"

# Response model
class DocumentationResponse(BaseModel):
    content: str
    format: OutputFormat
    message: str

@app.post(
    "/generate-documentation",
    response_model=DocumentationResponse,
    status_code=status.HTTP_201_CREATED
)
async def generate_documentation(request: DocumentationRequest):
    try:
        # Get the required data from database
        explanations = get_explanations()
        codebase_summary = get_codebase_summary()
        
        content = None  # Initialize content variable
        
        # Generate the actual documentation based on format
        if request.output_format == OutputFormat.LATEX:
            content = render_latex_document(
                explanations,
                codebase_summary,
                request.author_name
            )
        elif request.output_format == OutputFormat.MARKDOWN:
            content = render_markdown_document(
                explanations,
                codebase_summary,
                request.author_name
            )
        elif request.output_format == OutputFormat.WORD:
            # For Word, we need to handle it differently since it creates a file
            output_filename = "documentation.docx"
            render_word_document(
                explanations,
                codebase_summary,
                output_filename,
                request.author_name
            )
            # Read the generated Word file
            with open(output_filename, 'rb') as f:
                content = f.read()
            import os
            os.remove(output_filename)  # Clean up the file
        
        if content is None:
            raise ValueError("No content was generated")
            
        return DocumentationResponse(
            content=content,
            format=request.output_format,
            message=f"Documentation generated successfully in {request.output_format} format"
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate documentation: {str(e)}"
        )

# Health check endpoint
@app.get(
    "/health",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "API is healthy",
            "content": {
                "application/json": {
                    "example": {
                        "status": "healthy"
                    }
                }
            }
        }
    }
)
async def health_check():
    return {"status": "healthy"}