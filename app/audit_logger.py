import time
from datetime import datetime
from flask import request
from flask_login import current_user

class AuditLogger:
    @staticmethod
    def log_event(event_type, description, user_id=None, ip_address=None, metadata=None):
        """Registra eventos de segurança e auditoria"""
        timestamp = datetime.utcnow().isoformat()
        user_id = user_id or (current_user.id if current_user.is_authenticated else None)
        ip_address = ip_address or request.remote_addr if request else 'N/A'
        
        log_entry = {
            'timestamp': timestamp,
            'event_type': event_type,
            'description': description,
            'user_id': user_id,
            'ip_address': ip_address,
            'metadata': metadata or {}
        }
        
        # Formatar para log humano-legível
        human_log = f"[AUDIT] {timestamp} | {event_type} | User:{user_id} | IP:{ip_address} | {description}"
        
        # Log no console (em produção iria para arquivo/BD)
        print(human_log)
        
        # TODO: Em produção, salvar em banco de dados
        # save_to_database(log_entry)
        
        return log_entry
    
    @staticmethod
    def log_login(success=True, reason=None):
        """Log de tentativas de login"""
        metadata = {'success': success}
        if reason:
            metadata['reason'] = reason
            
        AuditLogger.log_event(
            'LOGIN_ATTEMPT',
            'Login successful' if success else f'Login failed: {reason}',
            metadata=metadata
        )
    
    @staticmethod
    def log_account_creation():
        """Log de criação de conta"""
        AuditLogger.log_event('ACCOUNT_CREATED', 'New user account created')
    
    @staticmethod
    def log_business_creation(business_id, business_name):
        """Log de criação de negócio"""
        AuditLogger.log_event(
            'BUSINESS_CREATED',
            f'Business created: {business_name}',
            metadata={'business_id': business_id, 'business_name': business_name}
        )
    
    @staticmethod
    def log_account_deletion():
        """Log de exclusão de conta"""
        AuditLogger.log_event('ACCOUNT_DELETED', 'User account deleted')
    
    @staticmethod
    def log_security_event(event_description, severity='MEDIUM'):
        """Log de eventos de segurança"""
        AuditLogger.log_event(
            'SECURITY_EVENT',
            event_description,
            metadata={'severity': severity}
        )

# Instância global do logger
audit_logger = AuditLogger()
