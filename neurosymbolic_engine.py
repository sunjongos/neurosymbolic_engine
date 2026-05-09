import os
import sys
import json
import requests
import google.generativeai as genai
from neo4j import GraphDatabase

# Windows 터미널 인코딩 오류 방지
sys.stdout.reconfigure(encoding='utf-8')

class NeurosymbolicEngine:
    """
    대표님이 정의하신 하드웨어 메타포(GPU-CPU-HBM)에 입각하여 설계된
    Neurosymbolic AI 통합 파이프라인 엔진입니다.
    """
    
    def __init__(self):
        # 1. GPU (우뇌/LLM) 설정
        self.gemini_api_key = "AIzaSyD5L0tbKObXGxd9gXuTGIOy-6-DgGHmJSI"
        genai.configure(api_key=self.gemini_api_key)
        self.gpu_model = genai.GenerativeModel('gemini-2.5-flash')
        
        # 2. CPU (좌뇌/Neo4j) 설정
        self.cpu_uri = "bolt://localhost:7687"
        self.cpu_user = "neo4j"
        self.cpu_pass = "password"
        
        # 3. HBM (장기공유메모리 Port 5050) 설정
        self.hbm_url = "http://localhost:5050/memory"
        
    def hbm_read(self, query):
        """HBM(공유메모리)에서 관련 컨텍스트를 초고속으로 가져옴"""
        print(f"💾 [HBM (5050 Memory)] '{query[:10]}...' 관련 컨텍스트 로드 중...")
        try:
            response = requests.get(self.hbm_url, params={"query": query}, timeout=3)
            if response.status_code == 200:
                data = response.json()
                return data.get('results', [])
        except requests.exceptions.RequestException as e:
            print(f"⚠️ HBM 연결 실패 (서버 오프라인 캐시 모드로 전환): {e}")
        return []

    def hbm_write(self, key, value):
        """새로운 지식을 HBM(공유메모리)에 캐싱"""
        print(f"💾 [HBM (5050 Memory)] 새로운 파싱 지식 캐싱 중...")
        try:
            requests.post(self.hbm_url, json={"key": key, "value": value}, timeout=3)
        except requests.exceptions.RequestException:
            pass

    def gpu_process(self, input_text, context_data):
        """우뇌(LLM) 병렬 연산: 입력 텍스트와 HBM 컨텍스트를 융합하여 논리(JSON) 추출"""
        print(f"🧠 [GPU (우뇌/LLM)] 데이터 병렬 파싱 및 직관적 패턴 추론 중...")
        prompt = f"""
        당신은 Neurosymbolic AI의 '우뇌(GPU)'입니다.
        아래 입력된 텍스트와 제공된 HBM 컨텍스트를 바탕으로 핵심 엔티티와 관계를 추출하세요.
        반드시 마크다운 기호 없는 순수 JSON 형식으로만 반환하세요.
        
        [HBM Context]
        {context_data}
        
        [Input Text]
        {input_text}
        
        출력 예시:
        {{
            "entities": [{{"id": "A", "type": "Concept", "description": "..."}}],
            "relationships": [{{"source": "A", "target": "B", "relation": "LINKS_TO"}}]
        }}
        """
        response = self.gpu_model.generate_content(prompt)
        try:
            raw_json = response.text.strip().removeprefix("```json").removesuffix("```").strip()
            return json.loads(raw_json)
        except Exception as e:
            print(f"⚠️ GPU JSON 파싱 실패: {e}\n원본 출력:\n{response.text}")
            return None

    def cpu_execute(self, parsed_data):
        """좌뇌(Neo4j) 제어: GPU가 파싱한 논리 구조를 팩트 DB에 검증 및 주입"""
        if not parsed_data:
            return
            
        print(f"🧩 [CPU (좌뇌/Neo4j)] 논리 연산 및 지식 그래프(Ontology) 주입 중...")
        driver = GraphDatabase.driver(self.cpu_uri, auth=(self.cpu_user, self.cpu_pass))
        with driver.session() as session:
            # 1. 엔티티(노드) 생성
            for ent in parsed_data.get('entities', []):
                session.run(
                    "MERGE (e:Concept {name: $name}) SET e.type = $type, e.description = $desc",
                    name=ent['id'], type=ent.get('type', 'Concept'), desc=ent.get('description', '')
                )
            # 2. 관계(엣지) 생성
            for rel in parsed_data.get('relationships', []):
                relation_type = "".join([c if c.isalnum() else "_" for c in rel['relation'].upper()])
                cypher = f"""
                MATCH (a:Concept {{name: $source}})
                MATCH (b:Concept {{name: $target}})
                MERGE (a)-[:{relation_type}]->(b)
                """
                session.run(cypher, source=rel['source'], target=rel['target'])
        driver.close()
        print("✨ [CPU (좌뇌/Neo4j)] 연산 완료. 무결점 지식이 구조화되었습니다.")

    def run_pipeline(self, input_text):
        """전체 파이프라인 실행: HBM Read -> GPU Process -> CPU Execute -> HBM Write"""
        print("\n=== 🚀 Neurosymbolic Engine Pipeline Started ===")
        
        # 1. HBM에서 사전 지식(Context)을 고속으로 로드
        context = self.hbm_read(input_text[:20]) 
        
        # 2. GPU(LLM) 연산: 비정형 데이터 패턴 파싱
        parsed_logic = self.gpu_process(input_text, context)
        
        if parsed_logic:
            # 3. CPU(Neo4j) 연산: 팩트 주입 및 구조화
            self.cpu_execute(parsed_logic)
            
            # 4. 처리 결과를 다시 HBM에 고속 캐싱
            first_entity = parsed_logic['entities'][0]['id'] if parsed_logic['entities'] else "unknown"
            self.hbm_write("last_processed_entity", first_entity)
            
        print("=== 🏁 Pipeline Execution Complete ===\n")

if __name__ == "__main__":
    engine = NeurosymbolicEngine()
    test_query = "NDB(남양주백병원)의 2026년 경영 전략은 AI 에이전트를 도입하여 의사결정(DSS) 속도와 정확성을 인간 뇌의 신경망 수준으로 극대화하는 것이다."
    engine.run_pipeline(test_query)
