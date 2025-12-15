import json
from typing import Optional, Dict, List

import redis.asyncio as aioredis

from config.logging_config import logger


class RedisService:
    """Service for managing Redis operations for seat booking."""

    def __init__(self, redis_url: str):
        """
        Initialize the Redis service.

        Args:
            redis_url: The Redis connection URL
        """
        self._redis_url = redis_url
        self._redis_client: Optional[aioredis.Redis] = None
        self.pubsub = None

    @staticmethod
    def seat_key(showtime_id: str, seat_id: str) -> str:
        """Generate the Redis key for a seat reservation."""
        return f"seat:{showtime_id}:{seat_id}"

    @staticmethod
    def purchase_key(showtime_id: str, seat_id: str) -> str:
        """Generate the Redis key for a seat purchase lock."""
        return f"seat:purchase:{showtime_id}:{seat_id}"

    @staticmethod
    def channel_name(showtime_id: str) -> str:
        """Generate the Redis pub/sub channel name for a showtime."""
        return f"showtime:{showtime_id}"

    async def connect(self):
        """Establish connection to Redis."""
        try:
            ssl_params = {}
            if self._redis_url.startswith("rediss://"):
                ssl_params = {"ssl_cert_reqs": None}

            self._redis_client = aioredis.from_url(
                self._redis_url, encoding="utf-8", decode_responses=True, **ssl_params
            )
            await self._redis_client.ping()
            logger.info("Successfully connected to Redis")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise

    async def disconnect(self):
        """Close Redis connection."""
        if self._redis_client:
            await self._redis_client.close()
            logger.info("Disconnected from Redis")

    async def reserve_seat(
        self, showtime_id: str, seat_id: str, user_id: str, ttl: int = 900
    ) -> bool:
        """
        Attempt to reserve a seat for a specific showtime by setting a unique key in Redis.

        Args:
            showtime_id: The unique identifier for the showtime.
            seat_id: The unique identifier for the seat to reserve.
            user_id: The user ID attempting to reserve the seat.
            ttl: Time-to-live in seconds for the reservation (default: 15 minutes).

        Returns:
            bool: True if the seat was successfully reserved (i.e., not already reserved), False otherwise.
        """
        key = self.seat_key(showtime_id, seat_id)
        try:
            result = await self._redis_client.set(key, user_id, nx=True, ex=ttl)
            if result:
                logger.info(
                    f"Seat {seat_id} reserved for user {user_id} in showtime {showtime_id}"
                )
                return True
            logger.warning(f"Seat {seat_id} already reserved in showtime {showtime_id}")
            return False
        except Exception as e:
            logger.error(f"Error reserving seat: {e}")
            return False

    async def release_seat(self, showtime_id: str, seat_id: str) -> bool:
        """
        Release a reserved seat by removing its reservation key from Redis.

        Args:
            showtime_id: The unique identifier for the showtime.
            seat_id: The unique identifier for the seat to release.

        Returns:
            bool: True if the seat was successfully released (key deleted), False otherwise.
        """
        key = self.seat_key(showtime_id, seat_id)
        try:
            result = await self._redis_client.delete(key)
            if result:
                logger.info(f"Released seat {seat_id} in showtime {showtime_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error releasing seat: {e}")
            return False

    async def get_seat_reservation(
        self, showtime_id: str, seat_id: str
    ) -> Optional[str]:
        """
        Retrieve the user ID who currently holds the reservation for a specific seat in a given showtime.

        Args:
            showtime_id: The unique identifier for the showtime.
            seat_id: The unique identifier for the seat whose reservation is being queried.

        Returns:
            Optional[str]: The user ID if the seat is reserved, or None if the seat is not reserved or an error occurs.
        """
        key = self.seat_key(showtime_id, seat_id)
        try:
            return await self._redis_client.get(key)
        except Exception as e:
            logger.error(f"Error getting seat reservation: {e}")
            return None

    async def get_all_reserved_seats(self, showtime_id: str) -> Dict[str, str]:
        """
        Get all reserved seats for a showtime.

        Args:
            showtime_id: The showtime ID

        Returns:
            Dict[str, str]: Dictionary mapping seat_id to user_id
        """
        pattern = f"seat:{showtime_id}:*"
        reserved_seats: Dict[str, str] = {}
        try:
            async for key in self._redis_client.scan_iter(match=pattern):
                seat_id = key.split(":")[-1]
                user_id = await self._redis_client.get(key)
                if user_id:
                    reserved_seats[seat_id] = user_id
            return reserved_seats
        except Exception as e:
            logger.error(f"Error getting reserved seats: {e}")
            return {}

    async def extend_reservation(
        self, showtime_id: str, seat_id: str, ttl: int = 900
    ) -> bool:
        """
        Extend the reservation time for a seat.

        Args:
            showtime_id: The showtime ID
            seat_id: The seat ID
            ttl: New time-to-live in seconds

        Returns:
            bool: True if extended, False otherwise
        """
        key = self.seat_key(showtime_id, seat_id)
        try:
            result = await self._redis_client.expire(key, ttl)
            if result:
                logger.info(f"Extended reservation for seat {seat_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error extending reservation: {e}")
            return False

    async def publish_seat_update(
        self, showtime_id: str, seat_id: str, status: str, user_id: Optional[str] = None
    ):
        """
        Publish a seat status update to the Redis pub/sub channel for real-time notifications.

        This method sends a message to the channel associated with the given showtime,
        informing subscribers about changes in seat status. Typical use cases include
        notifying frontends or other backend services when a seat is reserved, released,
        or purchased.

        Args:
            showtime_id: The unique identifier for the showtime.
            seat_id: The unique identifier for the seat whose status has changed.
            status: The new status of the seat (e.g., 'reserved', 'available', 'purchased').
            user_id: Optional; the user ID associated with the seat status change.
        """
        channel = self.channel_name(showtime_id)
        message = {
            "seat_id": seat_id,
            "status": status,
            "user_id": user_id,
            "showtime_id": showtime_id,
        }
        try:
            await self._redis_client.publish(channel, json.dumps(message))
            logger.debug(f"Published seat update to channel {channel}: {message}")
        except Exception as e:
            logger.error(f"Error publishing seat update: {e}")

    async def subscribe_to_showtime(self, showtime_id: str):
        """
        Subscribe to seat updates for a specific showtime.

        Args:
            showtime_id: The showtime ID

        Returns:
            PubSub: Redis pubsub object
        """
        channel = self.channel_name(showtime_id)
        pubsub = self._redis_client.pubsub()
        await pubsub.subscribe(channel)
        logger.info(f"Subscribed to channel {channel}")
        return pubsub

    async def get_seat_ttl(self, showtime_id: str, seat_id: str) -> int:
        """
        Get the remaining time-to-live (TTL) in seconds for a seat reservation in Redis.

        This method checks how many seconds remain before the reservation for a specific seat
        expires. It is useful for informing users or systems about how much longer a seat will
        remain reserved before it becomes available again.

        Args:
            showtime_id: The unique identifier for the showtime.
            seat_id: The unique identifier for the seat.

        Returns:
            int: Number of seconds until the reservation expires.
                 Returns -1 if the key exists but has no expiry (persistent).
                 Returns -2 if the key does not exist.
        """
        key = self.seat_key(showtime_id, seat_id)
        try:
            return await self._redis_client.ttl(key)
        except Exception as e:
            logger.error(f"Error getting seat TTL: {e}")
            return -2

    async def lock_seats_for_purchase(
        self, showtime_id: str, seat_ids: List[str], booking_id: str, ttl: int = 300
    ) -> bool:
        """
        Lock multiple seats for purchase process.

        Args:
            showtime_id: The showtime ID
            seat_ids: List of seat IDs to lock
            booking_id: The booking ID
            ttl: Time-to-live in seconds (default: 5 minutes)

        Returns:
            bool: True if all seats locked successfully
        """
        try:
            async with self._redis_client.pipeline() as pipe:
                for seat_id in seat_ids:
                    pipe.set(
                        self.purchase_key(showtime_id, seat_id),
                        booking_id,
                        nx=True,
                        ex=ttl,
                    )
                results = await pipe.execute()
                success = all(results)
                if success:
                    logger.info(
                        f"Locked {len(seat_ids)} seats for booking {booking_id}"
                    )
                else:
                    for seat_id in seat_ids:
                        await self._redis_client.delete(
                            self.purchase_key(showtime_id, seat_id)
                        )
                    logger.warning(f"Failed to lock all seats for booking {booking_id}")
                return success
        except Exception as e:
            logger.error(f"Error locking seats for purchase: {e}")
            return False

    async def unlock_seats_after_purchase(
        self, showtime_id: str, seat_ids: List[str]
    ) -> bool:
        """
        Unlock seats after successful purchase.

        Args:
            showtime_id: The showtime ID
            seat_ids: List of seat IDs to unlock

        Returns:
            bool: True if unlocked
        """
        try:
            for seat_id in seat_ids:
                await self._redis_client.delete(self.purchase_key(showtime_id, seat_id))
            logger.info(f"Unlocked {len(seat_ids)} seats after purchase")
            return True
        except Exception as e:
            logger.error(f"Error unlocking seats: {e}")
            return False
