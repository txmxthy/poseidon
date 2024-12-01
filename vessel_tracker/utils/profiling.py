import time
import cProfile
import pstats
from functools import wraps
from contextlib import contextmanager
from typing import Dict, Any, Optional
import logging


class PerformanceProfiler:
    """Utility class for tracking performance metrics and profiling."""

    def __init__(self):
        self.metrics: Dict[str, Any] = {}
        self.profiler = cProfile.Profile()

    @contextmanager
    def profile_section(self, section_name: str):
        """Context manager for profiling a section of code."""
        start_time = time.time()
        start_memory = self._get_memory_usage()

        try:
            yield
        finally:
            end_time = time.time()
            end_memory = self._get_memory_usage()

            self.metrics[section_name] = {
                'duration': end_time - start_time,
                'memory_delta': end_memory - start_memory
            }

    def profile_function(self, func_name: Optional[str] = None):
        """Decorator for profiling a function."""

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                section_name = func_name or func.__name__
                with self.profile_section(section_name):
                    return func(*args, **kwargs)

            return wrapper

        return decorator

    def start_profiling(self):
        """Start detailed CPU profiling."""
        self.profiler.enable()

    def stop_profiling(self, output_file: str = 'profile_stats.prof'):
        """Stop profiling and save results."""
        self.profiler.disable()
        self.profiler.dump_stats(output_file)

        # Print summary to console
        stats = pstats.Stats(self.profiler)
        stats.sort_stats('cumulative')
        stats.print_stats(20)  # Show top 20 time-consuming functions

    def _get_memory_usage(self) -> float:
        """Get current memory usage."""
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024  # MB
        except ImportError:
            return 0.0

    def print_metrics(self):
        """Print collected performance metrics."""
        print("\nPerformance Metrics:")
        print("-" * 50)
        for section, metrics in self.metrics.items():
            print(f"\n{section}:")
            print(f"  Duration: {metrics['duration']:.2f} seconds")
            if metrics['memory_delta'] > 0:
                print(f"  Memory Delta: {metrics['memory_delta']:.2f} MB")


# Initialize global profiler
profiler = PerformanceProfiler()
