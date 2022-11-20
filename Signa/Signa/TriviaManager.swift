//
//  TriviaManager.swift
//  triviapi
//
//  Created by Victoria Lucero on 11/11/22.
// IMPORTANTEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE a
// cuando se junte, poner el link de la api de la variable global,
// falta poner videos y/o imagenes
// y mandar a llamar a la api que cambia el resultado del quiz
//

import Foundation
import SwiftUI

class TriviaManager: ObservableObject{
    private(set) var trivia: [Trivia.Result] = []
    @Published private(set) var length = 0
    @Published private(set) var index = 0
    @Published private(set) var reachedEnd = false
    @Published private(set) var answerSelected = false
    @Published private(set) var question: AttributedString = ""
    @Published private(set) var answerChoices: [Answer] = []
    @Published private(set) var progress: CGFloat = 0.00
    @Published private(set) var score = 0
    //@State var topic : String = ""
    
    
    init(){
        Task.init{
            await fetchTrivia()
        }
    }
    func fetchTrivia() async{
        var endpoint = "letras1"
        if TriviaCategor != ""{
            endpoint = TriviaCategor
        }
        guard let url = URL(string: APIURL + "/quiz/\(endpoint)") else{
            fatalError("Missing URL")}
        let urlRequest = URLRequest(url: url)
        do{
            let(data, response) = try await URLSession.shared.data(for: urlRequest)
            
            guard (response as? HTTPURLResponse)?.statusCode == 200 else {fatalError("Error while fetching data")}
            
            let decoder = JSONDecoder()
            decoder.keyDecodingStrategy = .convertFromSnakeCase
            let decodeData = try decoder.decode(Trivia.self, from:data)
            
            DispatchQueue.main.async{
                self.index = 0
                self.score = 0
                self.progress = 0.00
                self.reachedEnd = false
                self.trivia = decodeData.results
                self.length = self.trivia.count
                self.setQuestion()
            }
        }
        catch{
            print("error fetching trivia: \(error)")
        }
        
    }
    func goToNextQuestion(){
        if index + 1 < length{
            index += 1
            setQuestion()
        }else{
        reachedEnd = true
           
        }
        
    }
    func  setQuestion(){
        answerSelected = false
        progress = CGFloat(Double(index + 1) / Double(length) * 350)
        if index < length {
            let currentTriviaQuestion = trivia[index]
           // question = currentTriviaQuestion.formattedQuestion
            answerChoices = currentTriviaQuestion.answers
        }
    }
    func selectAnswers(answer: Answer){
        answerSelected = true
        if answer.isCorrect{
            score += 1
        }
    }
    
}
