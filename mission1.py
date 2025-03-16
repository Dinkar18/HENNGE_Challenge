def main():
    import sys
    data = sys.stdin.read().splitlines()
    
    def process_cases(lines):
        if not lines:
            return []
        
        n = int(lines[0])  # Number of test cases
        cases = lines[1:]
        
        def process_case(remaining, results):
            if not remaining:
                return results
            
            x = int(remaining[0])  # Number of integers in the test case
            numbers = map(int, remaining[1].split())
            
            def positive_squares(nums, total=0):
                if not nums:
                    return total
                head, *tail = nums
                return positive_squares(tail, total + (head * head) if head >= 0 else total)
            
            return process_case(remaining[2:], results + [str(positive_squares(list(numbers)))])
        
        return process_case(cases, [])
    
    print("\n".join(process_cases(data)))

if __name__ == "__main__":
    main()
