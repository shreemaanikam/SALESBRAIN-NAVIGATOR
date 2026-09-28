import os

def patch_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    old_code = """class WorkspaceRegistry:
    \"\"\"Thread-safe (enough for single-worker demo) in-memory workspace store.\"\"\"

    def __init__(self):
        self._workspaces: Dict[str, Dict[str, Any]] = {}

    def create(self, dataset_id: str, filename: str, df: pd.DataFrame) -> Dict:
        ws = {
            "dataset_id": dataset_id,
            "filename": filename,
            "created_at": datetime.utcnow().isoformat(),
            "row_count": len(df),
            "column_count": len(df.columns),
            "df": df,
            "mapping": {},          # confirmed column mapping
            "profile": {},          # detected column roles
            "dashboard": None,      # computed analytics
            "insights": None,       # computed insights
            "recommendations": None, # computed recommendations
            "status": "uploaded",
        }
        self._workspaces[dataset_id] = ws
        logger.info(f"Workspace created: {dataset_id} ({filename}, {len(df)} rows)")
        return self._public(ws)

    def get(self, dataset_id: str) -> Optional[Dict]:
        return self._workspaces.get(dataset_id)

    def list(self) -> List[Dict]:
        return [self._public(ws) for ws in self._workspaces.values()]

    def update(self, dataset_id: str, **kwargs):
        if dataset_id in self._workspaces:
            self._workspaces[dataset_id].update(kwargs)

    def delete(self, dataset_id: str):
        self._workspaces.pop(dataset_id, None)

    def _public(self, ws: Dict) -> Dict:
        \"\"\"Return workspace metadata without the raw DataFrame.\"\"\"
        return {k: v for k, v in ws.items() if k != "df"}


workspace_registry = WorkspaceRegistry()"""

    new_code = """import os
from backend.app.db.database import SessionLocal, engine, Base
from backend.app.db.models import Workspace

Base.metadata.create_all(bind=engine)

class DBWorkspaceRegistry:
    \"\"\"Persistent workspace store using SQLAlchemy and local Parquet files.\"\"\"
    
    def __init__(self):
        self.upload_dir = os.path.join("backend", "app", "data", "uploads")
        os.makedirs(self.upload_dir, exist_ok=True)

    def create(self, dataset_id: str, filename: str, df: pd.DataFrame) -> Dict:
        filepath = os.path.join(self.upload_dir, f"{dataset_id}.parquet")
        # Ensure column names are strings before saving to parquet
        df.columns = df.columns.astype(str)
        df.to_parquet(filepath, index=False)
        
        ws_data = {
            "dataset_id": dataset_id,
            "filename": filename,
            "created_at": datetime.utcnow().isoformat(),
            "row_count": len(df),
            "column_count": len(df.columns),
            "status": "uploaded",
            "mapping": {},
            "profile": {},
        }
        
        db = SessionLocal()
        try:
            ws_model = Workspace(
                id=dataset_id,
                filename=filename,
                filepath=filepath,
                status="uploaded",
                mapping={},
                profile=ws_data, # Use profile column to store row/column counts initially
            )
            db.add(ws_model)
            db.commit()
            logger.info(f"Workspace created in DB: {dataset_id} ({filename}, {len(df)} rows)")
        finally:
            db.close()
            
        return self._public(ws_data)

    def get(self, dataset_id: str) -> Optional[Dict]:
        db = SessionLocal()
        try:
            ws_model = db.query(Workspace).filter(Workspace.id == dataset_id).first()
            if not ws_model:
                return None
            
            # Reconstruct the dict
            ws = {
                "dataset_id": ws_model.id,
                "filename": ws_model.filename,
                "status": ws_model.status,
                "created_at": ws_model.created_at.isoformat(),
                "mapping": ws_model.mapping or {},
                "dashboard": ws_model.dashboard,
                "insights": ws_model.insights,
                "recommendations": ws_model.recommendations,
                "filepath": ws_model.filepath,
            }
            # Merge profile
            if ws_model.profile:
                ws.update(ws_model.profile)
                
            # Load DataFrame lazily when requested?
            # Existing code expects `ws["df"]` to be available. We'll load it here.
            try:
                ws["df"] = pd.read_parquet(ws_model.filepath)
            except Exception as e:
                logger.error(f"Failed to load dataset file for {dataset_id}: {e}")
                ws["df"] = pd.DataFrame()
                
            return ws
        finally:
            db.close()

    def list(self) -> List[Dict]:
        db = SessionLocal()
        try:
            workspaces = db.query(Workspace).all()
            results = []
            for ws_model in workspaces:
                ws = {
                    "dataset_id": ws_model.id,
                    "filename": ws_model.filename,
                    "status": ws_model.status,
                    "created_at": ws_model.created_at.isoformat(),
                }
                if ws_model.profile:
                    ws.update(ws_model.profile)
                results.append(self._public(ws))
            return results
        finally:
            db.close()

    def update(self, dataset_id: str, **kwargs):
        db = SessionLocal()
        try:
            ws_model = db.query(Workspace).filter(Workspace.id == dataset_id).first()
            if ws_model:
                # If df is in kwargs, we need to save it to disk! (because compute_dashboard mutates it)
                if "df" in kwargs:
                    df = kwargs.pop("df")
                    df.columns = df.columns.astype(str)
                    df.to_parquet(ws_model.filepath, index=False)
                
                if "mapping" in kwargs:
                    ws_model.mapping = kwargs.pop("mapping")
                if "dashboard" in kwargs:
                    ws_model.dashboard = kwargs.pop("dashboard")
                if "insights" in kwargs:
                    ws_model.insights = kwargs.pop("insights")
                if "recommendations" in kwargs:
                    ws_model.recommendations = kwargs.pop("recommendations")
                if "status" in kwargs:
                    ws_model.status = kwargs.pop("status")
                
                # Any other kwargs go to profile
                if kwargs:
                    prof = dict(ws_model.profile) if ws_model.profile else {}
                    prof.update(kwargs)
                    ws_model.profile = prof
                    
                db.commit()
        finally:
            db.close()

    def delete(self, dataset_id: str):
        db = SessionLocal()
        try:
            ws_model = db.query(Workspace).filter(Workspace.id == dataset_id).first()
            if ws_model:
                if os.path.exists(ws_model.filepath):
                    os.remove(ws_model.filepath)
                db.delete(ws_model)
                db.commit()
        finally:
            db.close()

    def _public(self, ws: Dict) -> Dict:
        return {k: v for k, v in ws.items() if k not in ("df", "filepath")}

workspace_registry = DBWorkspaceRegistry()"""

    content = content.replace(old_code, new_code)
    
    with open(filepath, "w") as f:
        f.write(content)

patch_file("backend/app/services/workspace_service.py")
