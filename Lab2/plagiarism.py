# for Plagarism detection for two document
import heapq
import re
from typing import List, Tuple

class State:
    def __init__(self,x:int, y:int,cost: int,path:List[Tuple[int,int]]):
        self.x=x
        self.y=y
        self.cost=cost
        self.path=path
        
    def __lt__(self,other):
        return self.cost<other.cost

def levenshtein_distance(a:str, b:str)-> int:
    if len(a)< len(b):
        return levenshtein_distance(b,a)

    if len(b)==0:
        return len(a)

    prev_row =range(len(b) +1)
    for i, c1 in enumerate(a):
        curr_row =[i+ 1]
        for j, c2 in enumerate(b):
            insertions =prev_row[j +1]+ 1
            deletions= curr_row[j]+1
            substitutions=prev_row[j]+(c1!=c2)
            curr_row.append(min(insertions,deletions,substitutions))
        prev_row =curr_row

    return prev_row[-1]

def preprocess_text(text:str) ->List[str]:
    text =re.sub(r'[^\w\s]', '',text.lower())
    return [s.strip() for s in text.split('.') if s.strip()]

def heuristic(state:State, doc1:List[str],doc2:List[str])-> int:
    remaining1 =len(doc1)-state.x
    remaining2 = len(doc2)-state.y
    return abs(remaining1-remaining2)*5

def a_star_alignment(doc1:List[str],doc2: List[str])->List[Tuple[int, int]]:
    initial_state = State(0,0,0,[])
    heap = [(0,initial_state)]
    visited =set()

    while heap:
        _, curr_state=heapq.heappop(heap)

        if curr_state.x==len(doc1) and curr_state.y==len(doc2):
            return curr_state.path

        if (curr_state.x,curr_state.y) in visited:
            continue

        visited.add((curr_state.x,curr_state.y))

        if curr_state.x<len(doc1) and curr_state.y<len(doc2):
            cost = levenshtein_distance(doc1[curr_state.x],doc2[curr_state.y])
            new_state = State(curr_state.x + 1,curr_state.y + 1,curr_state.cost + cost,
                              curr_state.path + [(curr_state.x, curr_state.y)])
            priority = new_state.cost+heuristic(new_state,doc1,doc2)
            heapq.heappush(heap,(priority, new_state))

        if curr_state.x<len(doc1):
            new_state=State(
                curr_state.x+1,
                curr_state.y,
                curr_state.cost+ 5,
                curr_state.path)
            priority=new_state.cost+heuristic(new_state,doc1,doc2)
            heapq.heappush(heap, (priority, new_state))

        if curr_state.y<len(doc2):
            new_state=State(curr_state.x,
                curr_state.y+1,
                curr_state.cost+5,
                curr_state.path)
            priority=new_state.cost+heuristic(new_state,doc1,doc2)
            heapq.heappush(heap,(priority,new_state))
    return []

def detect_plagiarism(doc1:List[str],doc2:List[str],threshold:float = 0.8)-> List[Tuple[str,str,float, int]]:
    alignment =a_star_alignment(doc1,doc2)
    detected_cases=[]
    total_distance= 0

    for i, j in alignment:
        if i< len(doc1) and j<len(doc2):
            distance = levenshtein_distance(doc1[i],doc2[j])
            total_distance +=distance
            similarity=1-(distance/ max(len(doc1[i]),len(doc2[j])))
            if similarity>=threshold:
                detected_cases.append((doc1[i],doc2[j],similarity,distance))

    return detected_cases,total_distance

def analyze_results(detected_cases:List[Tuple[str,str,float,int]],total_distance:int,doc1:List[str],doc2:List[str]):
    total_sentences =max(len(doc1),len(doc2))
    avg_distance=total_distance/total_sentences if total_sentences>0 else 0

    if len(detected_cases)==total_sentences and total_distance ==0:
        doc_type ="Identical Documents"
        expected_output ="All sentences align perfectly with zero edit distance."
    elif len(detected_cases)>=total_sentences* 0.8:
        doc_type ="Slightly Modified Document"
        expected_output= "Most sentences align with a low edit distance."
    elif len(detected_cases)<=total_sentences * 0.2:
        doc_type ="Completely Different Documents"
        expected_output ="High edit distances for most alignments, indicating no plagiarism."
    else:
        doc_type ="Partial Overlap"
        expected_output ="The overlapping content aligns with a low edit distance, indicating potential plagiarism."

    print(f"\nAnalysis Type:{doc_type}")
    print(f" Output:{expected_output}")

    print(f"\nTotal Edit Distance:{total_distance}")
    print(f"Average Edit Distance per Sentence:{avg_distance:.2f}")

def main():
    path1 =input("Enter the path of the first .txt file: ")
    path2=input("Enter the path of the second .txt file: ")

    try:
        with open(path1,'r') as file1, open(path2,'r') as file2:
            text1=file1.read()
            text2=file2.read()

        doc1 =preprocess_text(text1)
        doc2=preprocess_text(text2)
        detected_cases,total_distance=detect_plagiarism(doc1,doc2)
        print("\nAnalysis Results:")
        analyze_results(detected_cases, total_distance,doc1,doc2)

        if detected_cases:
            print("\nPotential plagiarism detected:")
            for case in detected_cases:
                print(f"Similarity: {case[2]:.2f}")
                print(f"Edit Distance: {case[3]}")
                print(f"Document 1: {case[0]}")
                print(f"Document 2: {case[1]}")
                print()
        else:
            print("\nNo significant plagiarism detected.")

    except FileNotFoundError:
        print("Error: One or both of the specified files could not be found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()

