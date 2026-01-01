using UnityEngine;
using UnityEngine.Networking;
using System.Collections;
using System.IO;
using System;

public class AudioAutoLoader : MonoBehaviour
{
    [Header("Settings")]
    public string audioPath = @"C:\Aniketh\Coding\Unity\Utopia_verse\Assets\therapist_voice.mp3";
    public AudioSource audioSource;

    private DateTime lastModified;
    private float timer = 0f;

    void Start()
    {
        if (File.Exists(audioPath))
        {
            lastModified = File.GetLastWriteTime(audioPath);
            StartCoroutine(LoadAudioSafe());
        }
    }

    void Update()
    {
        timer += Time.deltaTime;
        if (timer > 1.0f)
        {
            timer = 0f;
            CheckForUpdate();
        }
    }

    void CheckForUpdate()
    {
        if (File.Exists(audioPath))
        {
            DateTime currentModified = File.GetLastWriteTime(audioPath);
            if (currentModified > lastModified)
            {
                Debug.Log("🎤 Change detected... Waiting for Python to finish...");
                lastModified = currentModified;
                // Don't load immediately! Start the safe waiter.
                StopAllCoroutines(); // Stop any previous attempts
                StartCoroutine(LoadAudioSafe());
            }
        }
    }

    IEnumerator LoadAudioSafe()
    {
        // 1. STABILITY CHECK
        // Wait until file size stops changing (Python is done writing)
        long fileSize = 0;
        long newSize = -1;
        
        // Loop until file size stays the same for 0.5 seconds
        while (fileSize != newSize)
        {
            fileSize = new FileInfo(audioPath).Length;
            yield return new WaitForSeconds(0.5f);
            newSize = new FileInfo(audioPath).Length;
        }

        // 2. LOAD
        string url = "file://" + audioPath;
        using (UnityWebRequest uwr = UnityWebRequestMultimedia.GetAudioClip(url, AudioType.MPEG))
        {
            yield return uwr.SendWebRequest();

            if (uwr.result == UnityWebRequest.Result.Success)
            {
                if (audioSource != null)
                {
                    AudioClip clip = DownloadHandlerAudioClip.GetContent(uwr);
                    audioSource.clip = clip;
                    audioSource.Play();
                    Debug.Log("✅ Voice Playing (Clean Start)");
                }
            }
            else
            {
                Debug.LogError("❌ Audio Error: " + uwr.error);
            }
        }
    }
}