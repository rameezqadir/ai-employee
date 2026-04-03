"""
Ralph Wiggum Loop
Monitors task completion autonomously until all tasks are done
"""
import time
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

vault_path = Path(os.getenv('VAULT_PATH', r'D:\ai-employee\AI_Employee_Vault'))
needs_action = vault_path / 'Needs_Action'
done = vault_path / 'Done'
log_dir = vault_path / 'Logs'
log_dir.mkdir(parents=True, exist_ok=True)

def count_pending_tasks():
    """Count tasks in Needs_Action"""
    return len(list(needs_action.glob('*.md')))

def log_status(iteration, pending, message=''):
    """Log current status"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    status = f'[{timestamp}] Iteration {iteration}: {pending} tasks pending'
    if message:
        status += f' - {message}'
    
    print(status)
    
    # Also log to file
    log_file = log_dir / 'ralph_loop.log'
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(status + '\n')

def run_ralph_loop(task_description='Process all pending tasks', 
                   max_iterations=10, 
                   check_interval=30):
    """
    Run autonomous task monitoring loop
    
    Args:
        task_description: What tasks to process
        max_iterations: Maximum number of check iterations
        check_interval: Seconds between checks
    """
    print('🤖 Ralph Wiggum Loop Starting...')
    print(f'📋 Task: {task_description}')
    print(f'🔄 Max iterations: {max_iterations}')
    print(f'⏱️  Check interval: {check_interval} seconds')
    print(f'📁 Monitoring: {needs_action}')
    print()
    
    for iteration in range(1, max_iterations + 1):
        pending = count_pending_tasks()
        
        print(f'{'='*60}')
        log_status(iteration, pending)
        
        # Check if all tasks complete
        if pending == 0:
            print()
            print('✅ All tasks complete!')
            log_status(iteration, pending, 'ALL COMPLETE')
            return True
        
        # List pending tasks
        print(f'\n📋 Pending tasks:')
        for idx, task_file in enumerate(needs_action.glob('*.md'), 1):
            print(f'   {idx}. {task_file.name}')
        
        # Wait before next check
        if iteration < max_iterations:
            print(f'\n⏳ Waiting {check_interval} seconds before next check...')
            time.sleep(check_interval)
        else:
            print(f'\n⚠️  Reached maximum iterations ({max_iterations})')
            log_status(iteration, pending, 'MAX ITERATIONS REACHED')
    
    print()
    print(f'⚠️  Loop completed with {pending} tasks still pending')
    print('💡 Tip: Increase max_iterations or check Claude Desktop for issues')
    
    return False

def main():
    """Main entry point"""
    import sys
    
    # Parse command line arguments
    task_desc = sys.argv[1] if len(sys.argv) > 1 else 'Process all pending tasks'
    max_iter = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    interval = int(sys.argv[3]) if len(sys.argv) > 3 else 30
    
    # Run the loop
    success = run_ralph_loop(task_desc, max_iter, interval)
    
    # Exit code
    import sys
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
