// Save as Sources/AppMain.swift
// Smallest SwiftUI app that builds. Replace ContentView with the real first screen.
import SwiftUI

@main
struct AppMain: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

struct ContentView: View {
    var body: some View {
        VStack(spacing: 12) {
            Image(systemName: "checkmark.seal.fill")
                .font(.system(size: 48))
            Text("It works")
                .font(.title2)
        }
        .padding()
    }
}
