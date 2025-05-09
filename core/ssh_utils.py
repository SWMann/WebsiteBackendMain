"""
SSH Tunnel utility functions for database connections
"""
import os
import sys
import atexit

# Check if sshtunnel is available
try:
    from sshtunnel import SSHTunnelForwarder

    SSHTUNNEL_AVAILABLE = True
except ImportError:
    SSHTUNNEL_AVAILABLE = False

# Global tunnel instance
_tunnel = None


def setup_ssh_tunnel():
    """
    Set up an SSH tunnel for database connections.
    Returns a tuple of (host, port) to use for the database connection.
    """
    global _tunnel

    # Only proceed if SSH tunneling is enabled and available
    use_ssh = os.environ.get('USE_SSH_TUNNEL', 'False') == 'True'

    if not use_ssh or not SSHTUNNEL_AVAILABLE:
        # Return direct connection parameters
        return (
            os.environ.get('DB_HOST', 'localhost'),
            os.environ.get('DB_PORT', '5432')
        )

    # SSH connection parameters
    ssh_host = os.environ.get('SSH_HOST', '')
    ssh_port = int(os.environ.get('SSH_PORT', '22'))
    ssh_user = os.environ.get('SSH_USER', '')
    ssh_password = os.environ.get('SSH_PASSWORD', '')
    ssh_key_file = os.environ.get('SSH_KEY_FILE', None)
    ssh_passphrase = os.environ.get('SSH_PASSPHRASE', None)

    # Remote database parameters
    remote_db_host = os.environ.get('REMOTE_DB_HOST', 'localhost')
    remote_db_port = int(os.environ.get('REMOTE_DB_PORT', '5432'))

    # Validation
    if not ssh_host or not ssh_user:
        print("SSH host or username not provided. Cannot establish tunnel.")
        return (
            os.environ.get('DB_HOST', 'localhost'),
            os.environ.get('DB_PORT', '5432')
        )

    try:
        # Determine authentication method
        tunnel_kwargs = {}
        if ssh_password:
            tunnel_kwargs['ssh_password'] = ssh_password
        elif ssh_key_file:
            tunnel_kwargs['ssh_pkey'] = ssh_key_file
            if ssh_passphrase:
                tunnel_kwargs['ssh_private_key_password'] = ssh_passphrase
        else:
            print("No SSH authentication method provided. Cannot establish tunnel.")
            return (
                os.environ.get('DB_HOST', 'localhost'),
                os.environ.get('DB_PORT', '5432')
            )

        # Create and start the tunnel
        _tunnel = SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_username=ssh_user,
            remote_bind_address=(remote_db_host, remote_db_port),
            local_bind_address=('127.0.0.1', 0),  # dynamically allocate local port
            **tunnel_kwargs
        )

        _tunnel.start()

        # Register function to close tunnel on exit
        atexit.register(close_ssh_tunnel)

        print(f"SSH tunnel established to {ssh_host}:{ssh_port} -> {remote_db_host}:{remote_db_port}")
        print(f"Database connecting through tunnel at 127.0.0.1:{_tunnel.local_bind_port}")

        # Return the tunnel's local binding for database connection
        return ('127.0.0.1', _tunnel.local_bind_port)

    except Exception as e:
        print(f"Error setting up SSH tunnel: {e}")
        print("Falling back to direct connection")

        return (
            os.environ.get('DB_HOST', 'localhost'),
            os.environ.get('DB_PORT', '5432')
        )


def close_ssh_tunnel():
    """Close the SSH tunnel if it exists."""
    global _tunnel

    if _tunnel and _tunnel.is_active:
        print("Closing SSH tunnel...")
        _tunnel.stop()
        _tunnel = None


def get_tunnel_status():
    """Return the status of the SSH tunnel."""
    global _tunnel

    if _tunnel:
        return {
            'active': _tunnel.is_active,
            'local_bind_address': f"127.0.0.1:{_tunnel.local_bind_port}" if _tunnel.is_active else None,
            'remote_bind_address': f"{_tunnel.ssh_host}:{_tunnel.ssh_port}" if _tunnel.is_active else None,
        }
    else:
        return {
            'active': False,
            'local_bind_address': None,
            'remote_bind_address': None,
        }