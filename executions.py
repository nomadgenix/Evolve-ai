from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from .. import models, schemas, database
from ..dependencies import get_current_user
from ..services import llm_service

router = APIRouter(
    prefix="/executions",
    tags=["executions"]
)

@router.get("/", response_model=List[schemas.Execution])
def get_executions(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get all executions for the current user's agents."""
    executions = db.query(models.Execution).join(
        models.Agent, models.Execution.agent_id == models.Agent.id
    ).filter(
        models.Agent.owner_id == current_user.id
    ).offset(skip).limit(limit).all()
    return executions

@router.post("/", response_model=schemas.Execution, status_code=status.HTTP_201_CREATED)
def create_execution(
    execution: schemas.ExecutionCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Create a new execution."""
    # Check if agent exists and belongs to user
    agent = db.query(models.Agent).filter(
        models.Agent.id == execution.agent_id,
        models.Agent.owner_id == current_user.id
    ).first()
    
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Create execution record
    db_execution = models.Execution(
        agent_id=execution.agent_id,
        input=execution.input,
        status="in_progress"
    )
    db.add(db_execution)
    db.commit()
    db.refresh(db_execution)
    
    # Process execution in background
    background_tasks.add_task(
        process_execution,
        db_execution.id,
        agent.model
    )
    
    return db_execution

@router.get("/{execution_id}", response_model=schemas.Execution)
def get_execution(
    execution_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get a specific execution by ID."""
    execution = db.query(models.Execution).join(
        models.Agent, models.Execution.agent_id == models.Agent.id
    ).filter(
        models.Execution.id == execution_id,
        models.Agent.owner_id == current_user.id
    ).first()
    
    if execution is None:
        raise HTTPException(status_code=404, detail="Execution not found")
    
    return execution

@router.delete("/{execution_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_execution(
    execution_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Delete an execution."""
    execution = db.query(models.Execution).join(
        models.Agent, models.Execution.agent_id == models.Agent.id
    ).filter(
        models.Execution.id == execution_id,
        models.Agent.owner_id == current_user.id
    ).first()
    
    if execution is None:
        raise HTTPException(status_code=404, detail="Execution not found")
    
    db.delete(execution)
    db.commit()
    return None

# Background task for processing executions
def process_execution(execution_id: int, model: str):
    """Process an execution in the background."""
    # Create a new database session for this background task
    db = next(database.get_db())
    
    try:
        # Get the execution
        execution = db.query(models.Execution).filter(models.Execution.id == execution_id).first()
        if not execution:
            return
        
        # Get the agent's input
        input_text = execution.input
        
        # Process with LLM
        try:
            output = llm_service.generate_response(input_text, model)
            execution.output = output
            execution.status = "completed"
        except Exception as e:
            execution.output = f"Error: {str(e)}"
            execution.status = "failed"
            
            # Log the error
            log = models.ExecutionLog(
                execution_id=execution.id,
                message=f"Error during execution: {str(e)}",
                level="error"
            )
            db.add(log)
        
        # Update execution record
        execution.completed_at = datetime.now()
        db.commit()
        
    except Exception as e:
        # Log any unexpected errors
        try:
            log = models.ExecutionLog(
                execution_id=execution_id,
                message=f"Unexpected error: {str(e)}",
                level="error"
            )
            db.add(log)
            db.commit()
        except:
            pass
    finally:
        db.close()
