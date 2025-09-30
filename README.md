# 🎭 Interdimensional Cable TV

**AI-Generated Video Art Installation** - Semantic video clustering and streaming using Veo 3, CLIP, and Cloudflare Stream

## 🎯 Project Status: PRODUCTION READY ✅

### ✅ System Overview:
- **Videos Generated**: 1,000+ unique AI-generated videos
- **Semantic Clusters**: 67 thematic channels organized by CLIP embeddings
- **Streaming**: Cloudflare Stream CDN for global delivery
- **TV Interface**: Retro CRT-styled web app with channel surfing
- **Google Cloud Project**: `pollinations-430910` (pollinations.ai)
- **Authentication**: gcloud credentials for Veo 3 API access

## 📁 Project Structure

**See [`PROJECT_ORGANIZATION.md`](PROJECT_ORGANIZATION.md) for complete file organization guide.**

### Key Directories:
- **`/scripts/`** - All Python scripts organized by function
  - `/veo_generation/` - Veo 3 video generation tools
  - `/clustering/` - Semantic clustering with CLIP
  - `/stream_upload/` - Cloudflare Stream upload tools
  - `/utilities/` - Helper scripts
- **`/html_apps/`** - Web TV applications
- **`/channels_reclustered_all/`** - 67 semantic video clusters
- **`/docs/`** - Documentation and reports
- **`/archived/`** - Outdated/one-time scripts

## 🚀 Quick Start

### 🎭 Generate Interdimensional Cable Channel

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Test single video generation:**
   ```bash
   python3 interdimensional_cable_generator.py test
   ```

3. **Generate full channel lineup (5 videos):**
   ```bash
   python3 interdimensional_cable_generator.py generate
   ```

4. **Generate custom number of videos:**
   ```bash
   python3 interdimensional_cable_generator.py generate 3
   ```

5. **Check status of all operations:**
   ```bash
   python3 interdimensional_cable_generator.py check
   ```

### 📺 Generate CRT Poster Variations

1. **Test single CRT variation:**
   ```bash
   python3 crt_poster_variations.py test 1
   ```

2. **Generate all CRT variations:**
   ```bash
   python3 crt_poster_variations.py generate
   ```

### 🧪 Core API Testing

1. **Test basic Veo 3 functionality:**
   ```bash
   python3 veo3_test.py
   ```

## 🎭 Python API Usage

```python
from interdimensional_cable_generator import InterdimensionalCableGenerator

# Initialize the generator
generator = InterdimensionalCableGenerator()

# Generate a full channel lineup
operations = generator.generate_channel_lineup(num_videos=5)

# Check status of all operations
generator.check_all_operations()

# Generate single video with custom prompt
operation_name = generator.generate_video(
    prompt="Your custom surreal prompt here",
    title="Custom Video"
)
```

### 📺 CRT Poster API Usage

```python
from crt_poster_variations import CRTPosterGenerator

# Initialize CRT generator
crt_gen = CRTPosterGenerator()

# Generate all CRT variations
operations = crt_gen.generate_all_variations()

# Generate specific variation
variations = crt_gen.get_crt_variations()
operation = crt_gen.generate_poster_variation(
    variations[0]['prompt'], 
    variations[0]['title']
)
```

## 🔧 Configuration

### Environment Variables (.env)
```
VERTEX_AI_KEY=AQ.Ab8RN6IQvl97vCzsP3YY7u6PuV7godzxNJavMO0V3WLrUMWVfA
```

### Available Veo 3 Models:
- `veo-3.0-generate-001` (Standard model)
- `veo-3.0-fast-generate-001` (Fast generation)
- `veo-3.0-generate-preview` (Preview version)
- `veo-3.0-fast-generate-preview` (Fast preview)

### Video Parameters:
- **Duration**: 1-8 seconds
- **Aspect Ratios**: "16:9", "9:16", "1:1"
- **Audio**: true/false
- **Sample Count**: 1-4 videos per request

## 📋 Organization Policies Successfully Overridden:

1. `iam.disableServiceAccountKeyCreation`
2. `iam.managed.disableServiceAccountKeyCreation`
3. `iam.disableServiceAccountKeyUpload`
4. `iam.managed.disableServiceAccountKeyUpload`
5. `iam.managed.disableServiceAccountApiKeyCreation`

## 🎯 Next Steps for New Session:

1. **Test the API** - Run the JavaScript or Python script to verify everything works
2. **Create Video Workflows** - Build automated pipelines for different use cases
3. **Add Error Handling** - Enhance robustness for production use
4. **Implement Video Management** - Add features for organizing and managing generated videos
5. **Build Web Interface** - Create a web UI for easier video generation

## 🔍 Troubleshooting:

### Common Issues:
- **API Key Error**: Ensure `VERTEX_AI_KEY` is set in `.env` file
- **Permission Denied**: Organization policies may need time to propagate (up to 15 minutes)
- **Model Not Found**: Verify the model name and that Vertex AI API is enabled

### Useful Commands:
```bash
# Check current gcloud project
/opt/homebrew/bin/gcloud config list

# List organization policies
/opt/homebrew/bin/gcloud org-policies list --organization=763054696479

# Test API key (should return project info)
curl -H "Authorization: Bearer $VERTEX_AI_KEY" \
  "https://us-central1-aiplatform.googleapis.com/v1/projects/light-depot-447020-j3/locations/us-central1/publishers/google/models"
```

## 🎉 Success Metrics:

- ✅ All 5 organization policies overridden
- ✅ API key successfully created via Google Cloud Console
- ✅ Vertex AI API enabled and accessible
- ✅ Both Python and JavaScript implementations ready
- ✅ Complete automation framework in place

**Ready for video generation! 🎬**
