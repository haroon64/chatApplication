from fastapi import WebSocket
from typing import List, Dict

# Global dictionary to keep track of all active WebSocket connections
CONNECTIONS = {}

class ConnectionManager:
    def __init__(self):
        """
        {
         group_id:[number of users ]
         }
         
        """
        """
        Initializes the ConnectionManager with an empty dictionary to store active connections.
        The dictionary maps group IDs to lists of WebSocket connections.
        """
        self.active_connections: Dict[int, List[WebSocket]] = CONNECTIONS

    async def connect(self, websocket: WebSocket, group_id: int):
        """
        Handles a new WebSocket connection.

        If the WebSocket is already connected under a different group_id, it will be removed
        from the old group before being added to the new group.

        Args:
            websocket (WebSocket): The WebSocket connection to manage.
            group_id (int): The ID of the group the WebSocket should be connected to.
        """
        await websocket.accept()  # Accept the incoming WebSocket connection

        # Check if the WebSocket is already connected under a different group_id
        for gid, connections in self.active_connections.items():
            if websocket in connections:
                # Remove the WebSocket from its current group
                connections.remove(websocket)
                if not connections:
                    # If the group has no more active connections, delete it
                    del self.active_connections[gid]
                break

        # Add the WebSocket to the new group_id
        if group_id in self.active_connections:
            self.active_connections[group_id].append(websocket)
        else:
            self.active_connections[group_id] = [websocket]

    def disconnect(self, websocket: WebSocket):
        """
        Disconnects a WebSocket from its associated group.

        This method removes the WebSocket from the list of active connections.
        If the group has no more active connections after removal, the group is deleted.

        Args:
            websocket (WebSocket): The WebSocket connection to disconnect.
        """
        for gid, connections in self.active_connections.items():
            if websocket in connections:
                connections.remove(websocket)
                if not connections:
                    # Delete the group if no active connections remain
                    del self.active_connections[gid]
                break

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """
        Sends a personal message directly to a single WebSocket connection.

        Args:
            message (str): The message to send.
            websocket (WebSocket): The WebSocket connection to send the message to.
        """
        await websocket.send_text(message)

    async def broadcast(self, message: str, group_id: int, sender: WebSocket):
        """
        Broadcasts a message to all WebSocket connections in a specified group, except the sender.

        Args:
            message (str): The message to broadcast.
            group_id (int): The ID of the group to broadcast the message to.
            sender (WebSocket): The WebSocket connection that sent the original message.

        Returns:
            bool: True if the message should be saved to the database (i.e., no recipients), 
                  otherwise False.
        """
        connections = self.active_connections.get(group_id, [])
        recipients = False  # Flag to check if there are any recipients

        for ws in connections:
            if ws != sender:
                recipients = True
                await ws.send_text(message)  # Send the message to the WebSocket
                return True  # Stop the loop once a message is successfully sent

        if not recipients:
            # If there were no recipients, log this and indicate the message should be saved
            print("No recipients found, possibly saving message to database.")
            return True  # Returning True to indicate the message should be saved
        
       