using System.Collections;
using System.IO;
using UnityEngine;
using UnityEngine.Networking;

public class MemoryLoader : MonoBehaviour
{
    [Header("Local File Settings")]
    // This is the path from your screenshot
    public string folderPath = "C:/Aniketh/Coding/sense/"; 
    public string fileName = "memory_color.png";

    [Header("Target Object")]
    public Renderer screenRenderer; // Drag your 360 Sphere or Plane here

    void Start()
    {
        if (screenRenderer == null)
            screenRenderer = GetComponent<Renderer>();

        // Start checking for the file
        StartCoroutine(LoadLocalFile());
    }

    IEnumerator LoadLocalFile()
    {
        // 1. Construct the path
        string fullPath = Path.Combine(folderPath, fileName);
        
        // Unity needs "file://" to read from disk
        string url = "file://" + fullPath;

        Debug.Log("🔍 Searching for memory at: " + fullPath);

        // 2. Safety Check (Verify file exists before trying to load)
        if (!File.Exists(fullPath))
        {
            Debug.LogError("❌ File not found! Did you run 'doctor.py' yet?");
            yield break; // Stop here if file is missing
        }

        // 3. Request the Texture
        using (UnityWebRequest request = UnityWebRequestTexture.GetTexture(url))
        {
            yield return request.SendWebRequest();

            if (request.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError("⚠️ Error Loading: " + request.error);
            }
            else
            {
                // 4. Apply the Texture
                Texture2D texture = DownloadHandlerTexture.GetContent(request);
                screenRenderer.material.mainTexture = texture;
                Debug.Log("✅ Memory Loaded from Sense folder!");
            }
        }
    }
    
    // Optional: Call this function to reload the image without restarting the game
    public void RefreshMemory()
    {
        StartCoroutine(LoadLocalFile());
    }
}