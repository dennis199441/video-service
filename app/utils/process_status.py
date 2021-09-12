from enum import Enum

class ProcessStatus(Enum):
  QUEUED = "QUEUED"
  RUNNING = "RUNNING"
  COMPLETED = "COMPLETED"
  CANCELLED ="CANCELLED"